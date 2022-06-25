import pandas as pd
import numpy as np
import datetime
from google.cloud import bigquery

bqclient = bigquery.Client()

def get_min_value(table_name, col_name):
  query_string_min = f"""
  SELECT MIN({col_name})
  AS FIRST_RIDE
  FROM `{table_name}`;
  """
  min = (
      bqclient.query(query_string_min)
      .result()
      .to_dataframe(
          # Optionally, explicitly request to use the BigQuery Storage API. As of
          # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
          # API is used by default.
          create_bqstorage_client=True,
      )
  )
  print(min)