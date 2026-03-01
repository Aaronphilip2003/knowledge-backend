import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

client = bigquery.Client()

DATASET = os.getenv("BQ_DATASET")
TABLE = os.getenv("BQ_TABLE")

def insert_entry(row: dict):
    table_id = f"{client.project}.{DATASET}.{TABLE}"
    errors = client.insert_rows_json(table_id, [row])
    return errors

def search_entries(query: str, limit: int = 10):
    table_id = f"{client.project}.{DATASET}.{TABLE}"

    sql = f"""
    SELECT *
    FROM `{table_id}`
    WHERE 
        LOWER(title) LIKE LOWER('%{query}%')
        OR LOWER(content) LIKE LOWER('%{query}%')
        OR LOWER(context) LIKE LOWER('%{query}%')
    ORDER BY created_at DESC
    LIMIT {limit}
    """

    query_job = client.query(sql)
    results = query_job.result()

    return [dict(row) for row in results]

def fetch_candidates(limit=500):
    table_id = f"{client.project}.{DATASET}.{TABLE}"

    sql = f"""
    SELECT *
    FROM `{table_id}`
    ORDER BY created_at DESC
    LIMIT {limit}
    """

    query_job = client.query(sql)
    results = query_job.result()

    return [dict(row) for row in results]