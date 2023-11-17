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
  



### Project 2: BigQuery Data Retrieval and Integration with GPT Assistant using Google Cloud Functions

- **Summary:**
  - Demonstrates integrating Google BigQuery with a GPT Assistant using Google Cloud Functions. A Python function handles HTTP requests, interacts with BigQuery to fetch data, and returns results in CSV format.
- **Workflow:**
  1. Develops a Python function (bigquery_connection) using BigQuery client and Flask for handling HTTP requests.
  2. Function executes a SQL query in BigQuery, retrieving media spend and client interactions data.
  3. Transforms query results into CSV format for ease of use with GPT Assistant.
  4. Packages the function with requirements.txt and deploys to Google Cloud Functions using gcloud CLI.
  5. Sets up an HTTP trigger for the function, making it accessible via a URL endpoint.
  6. Updates OpenAPI specifications of the GPT Assistant to include the Cloud Function's endpoint for seamless data integration.
  
