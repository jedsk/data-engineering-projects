# Data Engineering Portfolio

This repository contains a collection of data engineering projects, showcasing my skills and experience in the field. These projects demonstrate my expertise in various data engineering technologies and best practices.

## Projects

### [Project 1: Automated Daily Report Updater](https://github.com/jedsk/data-engineering-projects/blob/main/project1/project_1.ipynb)
- **Summary**: Automates updating daily reports in Google Sheets using Selenium, Google Sheets API, and Gmail API.
- **Key Features**:
  - Automates report downloads and updates in Google Sheets.
  - Utilizes Selenium for web interactions and Google APIs for data manipulation.
- **Technologies**: Python, Selenium, Google Sheets API, Gmail API, Pandas.

### [Project 2: BigQuery Data Retrieval and Integration with GPT Assistant](https://github.com/jedsk/data-engineering-projects/blob/main/project2/instructions.md)
- **Summary**: Integrates Google BigQuery with a GPT Assistant for digital marketing data analysis.
- **Key Features**:
  - Develops Python functions for HTTP requests and BigQuery queries.
  - Transforms query results into CSV for GPT Assistant integration.
  - Deploys functions to Google Cloud Functions.
- **Technologies**: Python, Google BigQuery, Google Cloud Functions, Flask.

### [Project 3: Comprehensive Audio Analysis and NLP with OpenAI and GCP](https://github.com/jedsk/data-engineering-projects/blob/main/project3/main.py)
- **Summary**: This project showcases the integration of OpenAI's Whisper API for audio transcription and GPT for detailed NLP analysis. It automates the extraction and analysis of key information from customer call transcripts, providing insights into customer interactions and sentiment.
- **Key Features**:
  - Credential management using GCP Secret Manager and automated login to ServiceTitan.
  - Automated downloading and uploading of audio files and transcripts to/from Google Cloud Storage (GCS).
  - Audio file transcription using OpenAI's Whisper API.
  - Detailed NLP analysis of transcriptions using OpenAI's GPT model to extract caller details, call type, urgency, and customer sentiment.
  - Formatting and saving analysis results in CSV format on GCS for easy interpretation and further use.
  - Comprehensive scripting that includes robust error handling and user-friendly functionality.
- **Deployment**:
  - The application is containerized and deployed to Google Cloud Run, ensuring scalable and efficient execution.
  - Docker is used for creating a container image of the application.
  - The container image is stored and managed using Google Artifact Registry, providing a secure and private storage solution for Docker images.
  - Deployment to Cloud Run is automated, allowing the application to be scaled up or down based on demand, and ensuring high availability.
- **Technologies Used**:
  - Python, OpenAI's Whisper and GPT APIs, Google Cloud Platform services (Secret Manager, Cloud Storage, Artifact Registry, and Cloud Run), Selenium WebDriver, Pandas, GCSFS, Docker.

