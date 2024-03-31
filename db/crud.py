import os
from google.cloud import bigquery
from .schema import Purchase

def save_data(client: bigquery.Client, data: any) -> None:
    try:
        query = f"""
            INSERT INTO {os.getenv('TABLE_ID')} (id, value, date)
            VALUES (@id, @value, @date);
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('id', 'STRING', data.id),
                bigquery.ScalarQueryParameter('value', 'FLOAT64', data.value),
                bigquery.ScalarQueryParameter('date', 'DATETIME', data.date)
            ]
        )

        client.query(query, job_config=job_config)
    except Exception as e:
        print(e)
        raise Exception('Error on saving to BigQuery table')


def get_data(client: bigquery.Client) -> list[Purchase]:
    try:
        query = f"""
            SELECT * FROM {os.getenv('TABLE_ID')}
        """

        job = client.query(query)
        return [Purchase(**dict(row)) for row in job.result()]
    except Exception as e:
        return []