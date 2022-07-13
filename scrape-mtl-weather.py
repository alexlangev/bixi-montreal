import requests
import datetime
from bs4 import BeautifulSoup
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import pandas as pd
import pandas_gbq

START_DATE = datetime.date(2014, 1, 1)
END_DATE = datetime.date(2022, 5, 31)
DATA_LABELS = ['DAY', 'Mean Temp', 'Total Rain', 'Total Snow', 'Spd of Max Gust']
TABLE_ID = 'bixi-montreal.bixi.mtl-weather'
PROJECT_ID = 'bixi-montreal'

# takes the month and year and return a BS4 object of the daily weather table of the corresponding month/year
def get_data_table(year, month):
  URL = f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?hlyRange=2013-02-13%7C2022-06-10&dlyRange=2013-02-14%7C2022-06-10&mlyRange=%7C&StationID=51157&Prov=QC&urlExtension=_e.html&searchType=stnProx&optLimit=yearRange&StartYear=1840&EndYear=2022&selRowPerPage=25&Line=10&txtRadius=25&optProxType=city&selCity=45%7C31%7C73%7C39%7CMontr%C3%A9al&selPark=&txtCentralLatDeg=&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongDeg=&txtCentralLongMin=0&txtCentralLongSec=0&txtLatDecDeg=&txtLongDecDeg=&timeframe=2&Day=10&Year={year}&Month={month}#'
  request = requests.get(URL)
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup.find('table', class_='data-table')

# takes the bs4 object of the table and a list of ('Strings') labels of the columns we want as argument and returns a dict with key:index, value: label
def get_table_dict(table, labels):
  col_dict = {}
  headers_list = table.find_all('th', scope='col')
  
  for th in headers_list:
    for label in labels:
      if label in th.get_text():
        col_dict[headers_list.index(th)] = label
  return col_dict

# takes year and month and return the number of days in it.
def number_of_days_in_month(year, month):
  return monthrange(year, month)[1]

# takes the bs4 object of the table, the data dict, the year and the month and returns a corresponding pandas dataframe
def get_dataframe(table, dict, year, month):
  monthly_data_dict = {}
  num_of_rows = number_of_days_in_month(year, month)
  all_rows = table.find('tbody').find_all('tr')[0:num_of_rows]

  # build dictionnary that will become the dataframe. keys are the column names and values are the lists of values from top to bottom of each column
  row_data_dict = {}
  for label in dict.values():
    row_data_dict[label] = []

  for row in all_rows:
    row_element_list = row.find_all(['th', 'td']) 
    for column_index in dict.keys():
      column_label = dict[column_index]
      # Interpret string and convert it into correct value
      value = row_element_list[column_index].get_text().strip()
      if(column_label == 'DAY'):
        value = datetime.datetime(year, month, int(value))
      elif(value == 'LegendMM'):
        value = None
      elif(value == 'LegendTT'):
        value = 0
      elif('LegendEE' in value):
        value = float(value.replace('LegendEE', ''))
      elif('<' in value):
        value = float(value.replace('<', ''))
      elif(value == ''):
        value = None
      else:
        value = float(value)
      row_data_dict[column_label].append(value)
  return pd.DataFrame.from_dict(row_data_dict)

# Loop through everymonth between START_DATE and END_DATE and append the corresponding data_frame to the main one.
bs4_table = get_data_table(START_DATE.year, START_DATE.month)
dictionnary = get_table_dict(bs4_table, DATA_LABELS)
main_df = pd.DataFrame()

# loop through months
inc_date = START_DATE
while(END_DATE >= inc_date):
  df = get_dataframe(bs4_table, dictionnary, inc_date.year, inc_date.month)
  main_df = pd.concat([df, main_df])
  print(f'{inc_date} completed!')
  inc_date += relativedelta(months=1)
  bs4_table = get_data_table(inc_date.year, inc_date.month)

# OOOPS... I   that gbq doesn't accept whitespace for column names... This should have been done earlier in the code.
formated_col_names = []
for name in main_df.columns:
  if name == 'DAY':
    formated_col_names.append('DATE')
  else:
    formated_col_names.append(name.upper().replace(' ', '_'))
main_df.columns = formated_col_names

# write the main_df to GBQ and pverwrites the existing table
pandas_gbq.to_gbq(dataframe = main_df, 
destination_table = TABLE_ID, 
project_id = PROJECT_ID, 
if_exists = 'replace')

print('Great Success!') 