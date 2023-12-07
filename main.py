import json
import time
import tempfile
import os
import pandas as pd
import gcsfs
import whisper
import soundfile as sf
import logging
import google.auth

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from google.cloud import secretmanager, storage
from google.oauth2 import service_account
from google import auth
from openai import OpenAI

# Constants
BUCKET_NAME = os.environ.get('BUCKET_NAME')
FOLDER_NAME = os.environ.get('FOLDER_NAME')
PROJECT_ID = os.environ.get('PROJECT_ID')
SECRET_NAME = os.environ.get('SECRET_NAME')
URL = os.environ.get('URL')
CALLS_REPORT_PATH = os.environ.get('CALLS_REPORT_PATH')
BASE_URL = os.environ.get('BASE_URL')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Functions
def get_secret(project_id, secret_name, secret_version):
    """Fetches a secret from GCP Secret Manager."""
    secret_client = secretmanager.SecretManagerServiceClient()
    secret_resource_id = f"projects/{project_id}/secrets/{secret_name}/versions/{secret_version}"
    secret_request = secretmanager.AccessSecretVersionRequest(name=secret_resource_id)
    secret_response = secret_client.access_secret_version(request=secret_request)
    return secret_response.payload.data.decode('UTF-8')


def parse_credentials(secret_value):
    """Parses credentials from a JSON secret."""
    try:
        credentials_json = json.loads(secret_value)
        return credentials_json['username'], credentials_json['password']
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in secret.")
    except KeyError:
        raise ValueError("Missing 'username' or 'password' in secret.")


def upload_to_gcs(bucket_name, source_file_name, folder_name):
    """Uploads a file to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    destination_path = f"{folder_name}/{os.path.basename(source_file_name)}"
    blob = bucket.blob(destination_path)

    print(f"Uploading {source_file_name} to {bucket_name}/{destination_path}") #logging    
   
    blob.upload_from_filename(source_file_name)
    print(f"Uploaded {source_file_name} to {destination_path}.")


def get_latest_downloaded_file(download_dir, file_extension):
    """Finds the most recently downloaded file in the specified directory with a given extension."""
    files = [os.path.join(download_dir, file) for file in os.listdir(download_dir) 
             if os.path.isfile(os.path.join(download_dir, file)) and file.endswith(file_extension)]
    return max(files, key=os.path.getctime, default=None)


def initialize_webdriver(download_dir):
    """Initializes the Chrome WebDriver with specified options for headless operation."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={download_dir}")
    chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--ignore-ssl-errors")

    # Set download preferences
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,  # Set the default download directory
        "download.prompt_for_download": False,       # Disable the download prompt
        "safebrowsing.enabled": True                 # Optional: Enable safe browsing
    })

    return webdriver.Chrome(options=chrome_options)


def login_to_servicetitan(driver, username, password):
    """Logs into ServiceTitan with provided credentials."""
    driver.get(URL)
    driver.find_element(By.NAME, "username").send_keys(username)
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)


def download_report(driver):
    """Navigates to the report page in ServiceTitan and downloads the report."""
    driver.get(CALLS_REPORT_PATH)
    time.sleep(10)
    # Click the date range input to select a date range
    driver.find_element(By.XPATH, '//input[@data-cy="qa-daterange-input"]').click()
    time.sleep(3)
    # Select a specific date range, e.g., "Yesterday"
    driver.find_element(By.XPATH, '/html/body/div[11]/div/div/div/div/div[1]/div[2]').click()
    # Run Report
    driver.find_element(By.XPATH, '//*[@id="app-base"]/div[2]/div[2]/div/div/div/div/div/div/form/div/div/div[2]/button').click()
    time.sleep(15)
    # Exporting CSV
    export_button = driver.find_element(By.XPATH, '//*[@id="app-base"]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/button')
    export_button.click()
    time.sleep(2)
    # Locate the 'Export' button in the modal and click it
    export_confirm_button = driver.find_element(By.XPATH, '//div[@role="alertdialog"]/div[3]/button')
    export_confirm_button.click()
    time.sleep(15)
    print("Download request completed.") #logging


def download_audio_files(driver, id_list, download_dir, bucket_name, parent_folder_name):
    """Downloads audio files for each call ID in the list."""
    # Calculate yesterday's date and format it as a folder name
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_folder_name = yesterday.strftime('%y%m%d')

    # Folder path in GCS
    gcs_folder_path = f"{parent_folder_name}/{yesterday_folder_name}"

    for call_id in id_list[:3]:  # Limit to first 3 for testing; remove slicing for full run
        try:
            video_page_url = f'{BASE_URL}{call_id}'
            driver.get(video_page_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
            
            # JavaScript to download the video as MP3
            download_script = """
            var videoElement = document.querySelector('video');
            var sourceElement = videoElement.querySelector('source');
            var url = sourceElement.src;
            var a = document.createElement('a');
            document.body.appendChild(a);
            a.style = 'display: none';
            a.href = url;
            a.download = 'call_recording_' + arguments[0] + '.mp3';
            a.click();
            window.URL.revokeObjectURL(url);
            """
            driver.execute_script(download_script, call_id)
            print(f"Download initiated for ID: {call_id}")
            time.sleep(5)

            downloaded_file_path = get_latest_downloaded_file(download_dir, '.mp3')

            if downloaded_file_path:
                upload_to_gcs(bucket_name, downloaded_file_path, gcs_folder_path)
            else:
                print(f"No audio file was downloaded for ID: {call_id}")
        except Exception as e:
            print(f"An error occurred while processing ID {call_id}: {e}")



def transcribe_audio_files(bucket_name, parent_folder, destination_folder):
    """Transcribes audio files from a GCS bucket using the Whisper model."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Calculate yesterday's date and format it as a folder name
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_folder_name = yesterday.strftime('%y%m%d')

    # Updated folder path in GCS
    source_folder = f"{parent_folder}/{yesterday_folder_name}"

    # Load Whisper model
    whisper_model = whisper.load_model("tiny.en")  # Adjust the model size as needed

    # List all audio files in the source folder
    blobs = bucket.list_blobs(prefix=source_folder)
    transcriptions = []

    for blob in blobs:
        if blob.name.endswith('.mp3'):
            print(f"Processing {blob.name}")

            # Create a temporary file and close it to use its path
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file_path = temp_file.name
            temp_file.close()

            try:
                # Download the file to the temporary file path
                blob.download_to_filename(temp_file_path)

                # Transcribe the audio file
                result = whisper_model.transcribe(temp_file_path)
                transcription = result['text']

                # Create a transcription record
                call_id = blob.name.split('/')[-1].replace('call_recording_', '').replace('.mp3', '')
                transcriptions.append({'ID': call_id, 'Transcription': transcription})
            finally:
                # Ensure the temporary file is deleted
                os.remove(temp_file_path)

    transcriptions_df = pd.DataFrame(transcriptions)
    
    # Generate CSV file name and path 
    csv_filename = f"transcriptions_{yesterday_folder_name}.csv"
    csv_file_path = os.path.join(tempfile.gettempdir(), csv_filename)
    transcriptions_df.to_csv(csv_file_path, index=False)

    # Upload the CSV file to GCS
    upload_to_gcs(bucket_name, csv_file_path, destination_folder)
    print("Transcription process completed.")

    # Remove the CSV file after uploading
    os.remove(csv_file_path)


def analyze_and_save_transcripts(bucket_name, source_folder, destination_folder, openai_api_key):
    """Analyzes transcribed audio files using OpenAI and saves the analysis to GCS."""
    storage_client = storage.Client()

    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%y%m%d')

    # Read the transcriptions CSV from GCS
    fs = gcsfs.GCSFileSystem(token=storage_client._credentials.token)
    source_csv_path = f"gs://{bucket_name}/{source_folder}/transcriptions_{yesterday_str}.csv"
    with fs.open(source_csv_path, 'rb') as f:
        transcriptions_df = pd.read_csv(f)

    # Initialize OpenAI client
    openai_client = OpenAI(api_key=openai_api_key)

    # Define the columns for the extracted details
    detail_columns = [
        "Caller Name", "Phone Number", "Call Type", "Service Type", "Call Reason", 
        "Urgency Level", "Tasks Extracted", "Customer Sentiment", "Agent Sentiment", 
        "Resolution Status", "Follow up Required", "Agent Name", "Agent Efficiency", 
        "Response Time", "Feedback Offered", "Upselling Attempt", "Repeat Call", "Data Privacy Adherence"
    ]

    # Add new columns to the DataFrame
    for column in detail_columns:
        transcriptions_df[column] = None

    # Process each transcript and append the details
    for index, row in transcriptions_df.iterrows():
        details_dict = analyze_transcript(openai_client, row['Transcription'])
        for key, value in details_dict.items():
            if key in detail_columns:
                transcriptions_df.at[index, key] = value.strip() if value else None

    # Save the updated DataFrame to GCS
    destination_csv_path = f"gs://{bucket_name}/{destination_folder}/analysis_{yesterday_str}.csv"
    with fs.open(destination_csv_path, 'w') as f:
        transcriptions_df.to_csv(f, index=False)

    print("Analysis and saving process completed.")



def analyze_transcript(client, transcript):
    """Uses OpenAI to analyze a transcript and extract key information."""
    prompt = (
        "Analyze the following call transcript and extract key details. "
        "Provide concise responses suitable for each. If details are not available, write NA. Do not include details in parenthesis:\n\n"
        "Transcript: {}\n\n"
        "Details to extract:\n"
        "- Caller Name\n"
        "- Phone Number\n"
        "- Call Type\n"
        "- Service Type\n"
        "- Call Reason\n"
        "- Urgency Level\n"
        "- Tasks Extracted\n"
        "- Customer Sentiment\n"
        "- Agent Sentiment\n"
        "- Resolution Status\n"
        "- Follow up Required\n"
        "- Agent Name\n"
        "- Agent Efficiency\n"
        "- Response Time\n"
        "- Feedback Offered\n"
        "- Upselling Attempt\n"
        "- Repeat Call\n"
        "- Data Privacy Adherence\n"
    ).format(transcript)

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4-1106-preview"  # or any other appropriate model
    )

    response_content = response.choices[0].message.content
    details_dict = {}
    for line in response_content.split("\n"):
        if "- " in line:
            key, value = line.split(": ")
            key = key.strip("- ").strip()
            details_dict[key] = value.strip()
    return details_dict


def main():
    username, password = parse_credentials(get_secret(PROJECT_ID, SECRET_NAME, 'latest'))

    download_dir = tempfile.mkdtemp()
    print(f"Download directory: {download_dir}") #logging
    driver = initialize_webdriver(download_dir)

    login_to_servicetitan(driver, username, password)
    download_report(driver)
    print("Files in download directory:", os.listdir(download_dir)) #logging
    downloaded_file_path = get_latest_downloaded_file(download_dir, '.xlsx')
    if downloaded_file_path:
        upload_to_gcs(BUCKET_NAME, downloaded_file_path, FOLDER_NAME)
    else:
        print("No file was downloaded.")

    df = pd.read_excel(downloaded_file_path, engine='openpyxl')
    id_list = df[df['Call Date'].notnull()]['ID'].tolist()

    download_audio_files(driver, id_list, download_dir, BUCKET_NAME, 'recordings')
    transcribe_audio_files(BUCKET_NAME, 'recordings', 'transcriptions')
    analyze_and_save_transcripts(BUCKET_NAME, 'transcriptions', 'analyses', OPENAI_API_KEY)

    driver.quit()
    print("Automation process completed.")

if __name__ == "__main__":
    main()
