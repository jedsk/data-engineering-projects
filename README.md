# Data Engineering Portfolio

This repository contains a collection of data engineering projects, showcasing my skills and experience in the field. These projects demonstrate my expertise in various data engineering technologies and best practices.

## Projects

### Project 1: [Automated Daily Report Updater for Google Sheets with Gmail API, Google Sheets API, and Selenium](https://github.com/jedsk/data-engineering-projects/blob/main/project_1.ipynb)

- **Summary:**
  - This data project automates the process of updating daily reports in Google Sheets using Selenium, Google Sheets API, Gmail API, and pandas for data transformation. The project consists of multiple functions handling specific tasks. By leveraging Selenium, Google APIs, and pandas, this project streamlines the process of updating daily reports in Google Sheets through automated data extraction, transformation, and updating tasks.
- **Workflow:**
  1. Functions using Selenium access the platform, filter reports, and download them, including Local Service Ads reports with custom date ranges
  2. The code reads Excel files and CSVs, converts data types, fills NaN values, and updates Google Sheets with the transformed data.
  3. Functions create dictionaries containing information about metrics and domains by reading data from a Google Sheet named "Daily Reporting Info."
  4. update_apa_reports() and update_domains_reports() functions loop through the dictionaries, read CSV files, and paste the data into specific worksheets within Google Sheets. They also update the number of rows left, "New data date," and "Last Updated" values.
  



### Project 2: [BigQuery Data Retrieval and Integration with GPT Assistant using Google Cloud Functions](https://github.com/jedsk/data-engineering-projects/blob/main/project2/instructions.md)

- **Summary**:
  - This project showcases the integration of Google BigQuery with a GPT Assistant via Google Cloud Functions. A Python function is developed to handle HTTP requests, perform queries on BigQuery, and return the results in CSV format, focusing on digital marketing data analysis.
- **Workflow:**
  1. Develops a Python function (bigquery_connection) using BigQuery client and Flask for handling HTTP requests.
  2. Function executes a SQL query in BigQuery, retrieving media spend and client interactions data.
  3. Transforms query results into CSV format for ease of use with GPT Assistant.
  4. Packages the function with requirements.txt and deploys to Google Cloud Functions using gcloud CLI.
  5. Sets up an HTTP trigger for the function, making it accessible via a URL endpoint.
  6. Updates OpenAPI specifications of the GPT Assistant to include the Cloud Function's endpoint for seamless data integration.
  
### Project 3: [Comprehensive Audio Analysis and NLP with OpenAI and GCP](https://github.com/jedsk/data-engineering-projects/blob/main/project3/instructions.md)

- **Summary**:
  - This advanced project integrates OpenAI's Whisper API for audio transcription and leverages GPT for a detailed Natural Language Processing (NLP) analysis. It automates the process of extracting and analyzing key information from customer call transcripts, offering insights into customer interactions, sentiment, and call details. The script also incorporates automated downloading and uploading of audio files and transcripts to and from Google Cloud Storage (GCS), providing a comprehensive solution for audio analysis and data processing.
- **Workflow:**
  1. Automates credential fetching from GCP Secret Manager and logs into ServiceTitan.
  2. Downloads reports and audio files from ServiceTitan and uploads them to Google Cloud Storage (GCS).
  3. Uses OpenAI's Whisper API to transcribe audio files stored in GCS.
  4. Processes transcriptions using OpenAI's GPT model to extract detailed information like caller name, call type, urgency level, and customer sentiment.
  5. Formats analysis results and saves them as structured data in CSV format on GCS for easy interpretation and further use.
  6. Combines downloading, transcribing, analyzing, and data management into a comprehensive script with robust error handling and logging.
  7. Designs the script for easy replication or modification for various audio analysis tasks, ensuring user-friendly functionality.

- **Technologies Used:**
  - Python for overall scripting.
  - OpenAI's Whisper and GPT APIs for audio transcription and NLP analysis.
  - Google Cloud Platform services, including Secret Manager and Cloud Storage.
  - Selenium WebDriver for automated web interactions.
  - Pandas for data manipulation and analysis.
  - GCSFS for interactions with Google Cloud Storage.
  - CSV format for data export and manipulation.
