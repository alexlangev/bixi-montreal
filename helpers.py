import pandas as pd
import numpy as np
import datetime
from google.cloud import bigquery

bqclient = bigquery.Client()

# takes in the gbq table names as a string and column name as a string and return the minimum value of that column.
def get_min_value(table_name, col_name):
  query_string = f"""
  SELECT MIN({col_name})
  AS FIRST_RIDE
  FROM `{table_name}`;
  """
  min = (
      bqclient.query(query_string)
      .result()
      .to_dataframe(
          create_bqstorage_client=True,
      )
  )
  return(pd.to_datetime(min.iat[0,0]).date())

# takes in the gbq table names as a string and column name as a string and return the maximum value of that column.
def get_max_value(table_name, col_name):
  query_string = f"""
  SELECT MAX({col_name})
  AS LATEST_RIDE
  FROM `{table_name}`;
  """
  max = (
      bqclient.query(query_string)
      .result()
      .to_dataframe(
          create_bqstorage_client=True,
      )
  )
  return(pd.to_datetime(max.iat[0,0]).date())

# takes in date and returns the number of daily users
def get_daily_count(date):
  query_string = f"""
  SELECT COUNT(*) 
  FROM `bixi-montreal.bixi.all-rides` 
  WHERE DATE(start_date) = '{date}'
  """

  count = (
    bqclient.query(query_string)
    .result()
    .to_dataframe(
        create_bqstorage_client=True,
    )
  )
  return count

# Takes in a start and end date and return the weather data as a dataframe
def get_weather_data(start_date, end_date):
  query_string = f"""
  SELECT *
  FROM `bixi-montreal.bixi.mtl-weather`
  WHERE DATE <= '{end_date}' AND DATE >= '{start_date}'
  """
  weather = (
    bqclient.query(query_string)
    .result()
    .to_dataframe(
        create_bqstorage_client=True,
    )
  )
  return weather