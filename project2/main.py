from google.cloud import bigquery
from flask import escape, make_response
import csv
import io

def bigquery_connection(request):
    # Construct BigQuery client object.
    client = bigquery.Client()

    # Define your BigQuery query here.
    query = """
        SELECT
          FORMAT_DATE('%Y-%m', date) as month,
          client,
          SUM(media_spend) as total_spend,
          SUM(clicks) AS clicks,
          SUM(impressions) AS impressions,
          SUM(revenue) AS revenue
        FROM
          `your_project.your_dataset.your_table`
        WHERE
          EXTRACT(YEAR FROM date) = 2023
        GROUP BY
          month, client
        ORDER BY
          month
    """
    query_job = client.query(query)  # API request

    # Wait for the query to complete and fetch the results
    results = query_job.result()

    # Convert the results to CSV
    proxy = io.StringIO()
    writer = csv.writer(proxy)
    # Write header
    writer.writerow([field.name for field in results.schema])
    # Write rows
    for row in results:
        writer.writerow(row.values())

    # Seek to start so `proxy` can be read from the beginning
    proxy.seek(0)
    
    # Create a response object with the CSV data as the body
    response = make_response(proxy.getvalue())
    # Set the appropriate headers for CSV
    cd = 'attachment; filename=my_report.csv'
    response.headers['Content-Disposition'] = cd
    response.headers['Content-Type'] = 'text/csv'
    
    return response
