from flask import Flask, request, session
from twilio.twiml.voice_response import VoiceResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import glob
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'something-in-the-water12423'  # Set a secret key for session handling

# Instantiate the OpenAI client with API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def export_conversation(conversation_history, folder_name):
    directory = os.path.join("conversations", folder_name)
    os.makedirs(directory, exist_ok=True)
    filename = os.path.join(directory, "conversation.txt")
    with open(filename, 'w') as file:
        for message in conversation_history:
            role = message['role']
            content = message['content']
            file.write(f"{role}: {content}\n")

def delete_old_files(folder_name):
    directory = os.path.join("conversations", folder_name)
    files = glob.glob(os.path.join(directory, "conversation_*.txt"))
    for file in files:
        os.remove(file)

def get_existing_appointments(sheet):
    # Retrieve all rows from the Google Sheet
    rows = sheet.get_all_values()

    # Extract the appointment dates, times, and stylists from the rows
    appointments = []
    for row in rows[1:]:  # Skip the header row
        date = row[1]
        time = row[2]
        stylist = row[6]
        if date and time and stylist:
            appointments.append((date, time, stylist))

    return appointments


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    # Retrieve the caller's phone number from the incoming request
    caller_number = request.values.get('From', 'Unknown number')

    """Respond to incoming phone calls and interact using GPT."""
    resp = VoiceResponse()

    # Check if there is incoming speech from the call
    if 'SpeechResult' in request.values:
        current_date = datetime.now().strftime("%m/%d/%Y")    
        
        incoming_msg = request.values['SpeechResult'].strip()

        # Retrieve the conversation history and folder name from the session
        conversation_history = session.get('conversation_history', [])
        folder_name = session.get('folder_name')

        # Append the user's message to the conversation history
        conversation_history.append({"role": "user", "content": incoming_msg})

        print("Updated conversation history:", conversation_history)

        # Retrieve the existing appointments from the Google Sheet
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Anyone\OneDrive\Desktop\python-twilio\credentials.json', scope)
            sheets_client = gspread.authorize(creds)
            sheet_url = 'https://docs.google.com/spreadsheets/d/1IwBNjCZ7xi2E8yZrSS0pQXfGepBLlzdt8h5JSIqsqR0/edit#gid=0'
            sheet = sheets_client.open_by_url(sheet_url).sheet1

            existing_appointments = get_existing_appointments(sheet)
        except Exception as e:
            print(f"Error occurred while retrieving existing appointments: {str(e)}")
            existing_appointments = []

        # Prepare the system message with existing appointments
        system_message = f"""
        You are a helpful and friendly hair salon receptionist. Your task is to assist customers
        in booking appointments, answering their questions, and gathering essential information.

        Please collect the customer's name, phone number, the service they request, and the preferred date and time for their appointment. 
        Aim to ask no more than two questions at a time to keep the conversation natural and engaging.

        When requesting the customer's phone number, inquire if they would like to use the number from which they are calling, which is {caller_number}.

        Salon Details:
        Our salon operates from Tuesday to Saturday, 9:00 AM to 6:00 PM.
        We are pleased to offer the expertise of three stylists:
        - Mia, who specializes in men's haircuts.
        - Lucas, known for women's haircuts.
        - Sofia, our expert in coloring.

        We offer a range of services including women's haircuts, men's haircuts, and coloring.
        Today's date is {current_date}.
        """

        system_message += "\n\nExisting Appointments:\n"
        for appointment in existing_appointments:
            system_message += f"- Date: {appointment[0]}, Time: {appointment[1]}, Stylist: {appointment[2]}\n"

        print(system_message)

        # Conditional logic based on caller's input
        if "price" in incoming_msg.lower() or "cost" in incoming_msg.lower():
            system_message += "\n\nThe caller has inquired about pricing. Please provide information about our service prices. Womens haircut: $50. Men's haircut: $40. Coloring: Starting from $80."
        elif "promotion" in incoming_msg.lower() or "discount" in incoming_msg.lower():
            system_message += "\n\nThe caller has inquired about promotions or discounts. Please inform them about any ongoing promotions or discounts we are offering."
        elif "cancel" in incoming_msg.lower() or "reschedule" in incoming_msg.lower():
            system_message += "\n\nThe caller wants to cancel or reschedule an appointment. Please assist them with the cancellation or rescheduling process."
        

        # Generate a response using OpenAI's GPT
        completion = client.chat.completions.create(
            model="gpt-4-turbo",  # Use a smaller model for faster response times
            messages=[
                {"role": "system", "content": system_message},
                *conversation_history
            ],
            max_tokens=100,  # Reduce the max_tokens for faster response times
            temperature=0.7,
            top_p=1  # Slightly lower top_p for more focused responses
        )

        # Use the GPT-generated answer in the voice response
        gpt_response = completion.choices[0].message.content
        resp.say(gpt_response, voice='Polly.Joanna-Neural')

        # Append the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": gpt_response})

        # Store the updated conversation history in the session
        session['conversation_history'] = conversation_history

        # Export the conversation history to the main file in the specific folder
        export_conversation(conversation_history, folder_name)

        # Gather the user's speech input again
        gather = resp.gather(input='speech', action='/answer', method='POST')
    else:
        # Generate a unique folder name for the new call
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"call_{timestamp}"
        session['folder_name'] = folder_name

        # Greet the caller and prompt them to speak
        gather = resp.gather(input='speech', action='/answer', method='POST')
        gather.say("Thank you for calling our salon. How may I assist you today?", voice='Polly.Joanna-Neural')

    return str(resp)


@app.route("/hangup", methods=['POST'])
def hangup():
    print("Hangup route triggered")

    try:
        # Find the newest folder in the "conversations" directory
        conversations_dir = "C:\\Users\\Anyone\\OneDrive\\Desktop\\python-twilio\\conversations"
        print(f"Looking for newest folder in: {conversations_dir}")
        
        folders = [f for f in os.listdir(conversations_dir) if os.path.isdir(os.path.join(conversations_dir, f))]
        print(f"Found folders: {folders}")
        
        newest_folder = max(folders, key=lambda f: os.path.getmtime(os.path.join(conversations_dir, f)))
        print(f"Newest folder: {newest_folder}")

        # Open the text file in the newest folder
        file_path = os.path.join(conversations_dir, newest_folder, "conversation.txt")
        print(f"Reading conversation from file: {file_path}")
        
        with open(file_path, 'r') as file:
            conversation_text = file.read()

        print("Conversation from the newest folder:")
        print(conversation_text)

        # Get current datetime in the desired format
        current_datetime = datetime.now().strftime("%m/%d/%Y %I:%M %p")
        current_date = datetime.now().strftime("%m/%d/%Y")

        # Analyze the conversation text using GPT
        prompt = f"""
        Today's date is {current_date}. Please analyze the following call transcript and interpret any relative dates (like 'tomorrow' or 'next Monday') based on today's date.
        Convert them into absolute dates in the format mm/dd/yyyy.

        Transcript:
        {conversation_text}

        Extract the following details:
        - Date (format mm/dd/yyyy)
        - Time (format hh:mm AM/PM)
        - Name
        - Phone Number (XXX) XXX-XXXX)
        - Stylist Requested
        - Service Requested
        """
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a call analysis assistant. Your task is to analyze the given call transcript and extract the requested details, ensuring to convert relative dates based on the provided today's date. Please provide the details in a structured format, using 'N/A' for missing information, like this:\nDate: [value]\nTime: [value]\nName: [value]\nPhone Number: [value]\nStylist Requested: [value]\nService Requested: [value]"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7,
            top_p=1
        )

        analysis_result = completion.choices[0].message.content
        print("GPT Analysis Result:")
        print(analysis_result)

        # Extract the details from the structured GPT response
        details = {}
        for line in analysis_result.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                details[key.strip()] = value.strip()

        print("\nExtracted Details:")
        print(details)

        # Authenticate and access the Google Sheet
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Anyone\OneDrive\Desktop\python-twilio\credentials.json', scope)
            sheets_client = gspread.authorize(creds)
            sheet_url = 'https://docs.google.com/spreadsheets/d/1IwBNjCZ7xi2E8yZrSS0pQXfGepBLlzdt8h5JSIqsqR0/edit#gid=0'
            sheet = sheets_client.open_by_url(sheet_url).sheet1

            # Append the data to the Google Sheet
            row_data = [
                current_datetime,
                details.get('Date', 'N/A'),
                details.get('Time', 'N/A'),
                details.get('Name', 'N/A'),
                details.get('Phone Number', 'N/A'),
                details.get('Service Requested', 'N/A'),
                details.get('Stylist Requested', 'N/A')
            ]
            print(f"Row data to be appended: {row_data}")
            sheet.append_row(row_data)
            print("Data pushed to Google Sheets successfully.")
        except gspread.exceptions.APIError as e:
            print(f"Google Sheets API Error: {str(e)}")
        except Exception as e:
            print(f"Error occurred while appending data to Google Sheets: {str(e)}")

    except FileNotFoundError as e:
        print(f"Error: Conversation file not found - {str(e)}")
    except Exception as e:
        print(f"Error occurred while processing conversation: {str(e)}")

    return '', 200

if __name__ == "__main__":
    app.run(debug=True)
