# Data Engineering Portfolio

This repository contains a collection of data engineering projects, showcasing my skills and experience in the field. These projects demonstrate my expertise in various data engineering technologies and best practices.

## Projects

### Project 1: [Automated Daily Report Updater for Google Sheets with Gmail API, Google Sheets API, and Selenium](https://github.com/jedsk/data-engineering-projects/blob/main/project_1.ipynb)

- **Summary:**
  - This data project automates the process of updating daily reports in Google Sheets using Selenium, Google Sheets API, Gmail API, and pandas for data transformation. The project consists of multiple functions handling specific tasks.
- **Workflow:**
  1. Functions using Selenium access the platform, filter reports, and download them, including Local Service Ads reports with custom date ranges
  2. The code reads Excel files and CSVs, converts data types, fills NaN values, and updates Google Sheets with the transformed data.
  3. Functions create dictionaries containing information about metrics and domains by reading data from a Google Sheet named "Daily Reporting Info."
  4. update_apa_reports() and update_domains_reports() functions loop through the dictionaries, read CSV files, and paste the data into specific worksheets within Google Sheets. They also update the number of rows left, "New data date," and "Last Updated" values.
  
 - By leveraging Selenium, Google APIs, and pandas, this project streamlines the process of updating daily reports in Google Sheets through automated data extraction, transformation, and updating tasks.



  
