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
  
### Project 3: [Whisper API and NLP Analysis with OpenAI](https://github.com/jedsk/data-engineering-projects/blob/main/project3/instructions.md)

- **Summary**:
  - This project demonstrates the utilization of OpenAI's Whisper API for transcribing audio recordings, followed by a comprehensive NLP analysis using OpenAI's GPT model. It focuses on extracting and analyzing key information from call transcripts for insights into customer interactions.
- **Workflow:**
  1. Transcribes an audio file using Whisper API, selecting the appropriate model size based on accuracy and performance needs.
  2. Processes the transcript with OpenAI's GPT model to extract critical details from the conversation, such as caller name, call type, urgency level, and customer sentiment.
  3. Formats the analysis results and processes them into structured data, converting them into a CSV format for easier interpretation and further use.
  4. Develops a comprehensive script combining the transcription and NLP analysis, ensuring seamless integration between different components.
  5. Implements error handling and logging for robustness, especially in cases where the transcript details do not match the expected format.
  6. Encapsulates the functionality in a user-friendly manner, allowing for easy replication or modification for different types of audio analysis tasks.
- **Technologies Used:**
  - Python, OpenAI's Whisper and GPT APIs, Pandas for data manipulation, and CSV for data export.
