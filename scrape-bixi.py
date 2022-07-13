# imports
import requests
import io
from bs4 import BeautifulSoup
from zipfile import ZipFile
import pandas as pd
import pandas_gbq

# variables
BIXI_URL = 'https://bixi.com/fr/donnees-ouvertes'
TABLE_ID = 'bixi-montreal.bixi.all-rides'
PROJECT_ID = 'bixi-montreal'
isReplace = True

# get html from website and create soup object
request = requests.get(BIXI_URL)
soup = BeautifulSoup(request.text, 'html.parser')

# create a list of all anchors on the page
open_data_wrapper= soup.find('div', class_="open-data-history")
data_sets_anchors = open_data_wrapper.find_all('a')

# for every anchor, get the zip files
for a in data_sets_anchors:
  href = a.get('href')
  response = requests.get(href, stream=True)
  
  # for every zip file, extract the csv file if it doesn't have 'stations' in the name and has 'od' or 'donnes_ouvertes' in the name.
  with ZipFile(io.BytesIO(response.content)) as zip:
    file_names = zip.namelist()
    
    for file_name in file_names:
      if 'STATIONS' not in file_name.upper() and ('OD' in file_name.upper() or 'DONNEES_OUVERTES' in file_name.upper()):
        with zip.open(file_name) as file:

          dataframe = pd.read_csv(file)
          
          # if the dataframe has a column named 'emplacement_pk_start', rename it to 'start_station_code'
          # if the dataframe has a column named 'emplacement_pk_end', rename it to 'end_station_code'

          if 'emplacement_pk_start' in dataframe.columns:
            dataframe.rename(columns = {'emplacement_pk_start':'start_station_code', 'emplacement_pk_end':'end_station_code'}, inplace = True)

          # set the code columns as str (It would be a better option to set them as int, but some rows have some letters in them)
          # and set the start and end datetime columns as datetime
          dataframe.start_station_code = dataframe.start_station_code.astype(str)
          dataframe.end_station_code = dataframe.end_station_code.astype(str)
          dataframe.start_date = pd.to_datetime(dataframe.start_date)
          dataframe.end_date = pd.to_datetime(dataframe.end_date)

          # write to big query per csv file. The first one overwrites the table, the others append to it.
          pandas_gbq.to_gbq(dataframe = dataframe, 
          destination_table = TABLE_ID, 
          project_id = PROJECT_ID, 
          if_exists = 'replace' if isReplace else 'append',
          api_method = 'load_csv')

          isReplace = False
          print(file_name, 'was added to the table bixi-montreal table in gbq')
