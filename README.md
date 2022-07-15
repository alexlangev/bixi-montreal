# Predicting daily users of Bixi Montreal

## Introduction
[Bixi](https://bixi.com/en) is Montreal's public bike share program. It has been in service since 2014 and now has close to 800 stations with close to 10000 bikes in the network. A team of drivers and technicians has to manually move bicycles from filled stations to empty ones. For this reason, predicting the amount of daily uses could help with scheduling employees and in turn, save money.

## Goal
Collect Bixi's daily usage data. For each day of service, collect the weather data of Montreal. Once the data collected and cleaned, train a linear regression model to predict the amount of daily rides based on the weather conditions.

## Data collection

1. Bixi has an [open data page](https://bixi.com/en/open-data) where you can find zipped monthly files of data. Downloading and unzipping and naming them properly is too error prone since there are more than 60 of them. This is why I decided to scrape them.

<p align="center">
  <img src="images\bixi-bike.jpg" alt="bixi data" width="850"/>
</p>
2. As for the weather, the [Canadian government](https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=51157&timeframe=2&StartYear=1840&EndYear=2022&Day=13&Year=2014&Month=4#) has daily and hourly history of different weather station's data, and one of them is in Montreal. 

<p align="center">
  <img src="images\montreal-daily-weathr.jpg" alt="weather data" width="850"/>
</p>

## Data cleaning

The only cleaning I had to do was:
- Convert the DAILY_COUNT column to an int
- Replace the NAN values int the different columns with the previous day's values.

## Feature engineering

The feature engineering was very simple 
- Query the count of rows per date and display that count in a column called DAILY_COUNT.
- Replace the datetime column to three columns, Day, Month and Year.

<p align="center">
  <img src="images\main.jpg" alt="main dataframe" width="850"/>
</p>

## Observations

- The daily count boxplot reveals that the datset is very symetric. The quartiles show that 50% of the daily rides throught the year is between 14000 and 26000.
- The most Bixi rides in a single day reached over 52000 rides.
- There seems to be a positive correlation between the daily weather and the total rides. That being said, there is high variance.
- There seems to be a negative correlation between the total rainfall and the total rides. 
- There is probably a negative correlation between snowfall and total rides. That being said, the dataset is highly skewed towards days with 0mm of snowfall. This is to be expected since the Bixi service is not offered during the winter months in Montreal. Therefore, there might not be enough datapoints to conclude a precise correlation.
- Days of the week were somewhat surprising. Sunday is the least popular day while Wednesday, Thursday and Friday are neck and neck for the most popular day.
- Months of the year show a bigger difference than days of the week. April and November are the least popular. That being said, Bixi's service is only offered for half of those months. December to March there are no rides since the service is not offered. Lastly, October is the least popular month the has the service running all month.
- As for year to year, there is a pretty clear increase since 2014. Because of Covid, 2020 dropped by almost 50% the previous year's usage. The year 2021 almost caught up with 2019's popularity. It is quite good considering that the province of Québec had some restrictions due to covid and work from home was heavily suggested by the provincial government.
- We are in the middle of 2022 and so data is still coming in. It seems to be back to it's pre-covid popularity.
- Until now (we are in June 2022), the year is breaking monthly records for every month.

## Conclusion

My model got a score of 0.74 with R^2 score test. I have no frame of reference on this value but it doesn't sound too bad for this use case. That being said, Predicting the daily rides of June 2022 was somewhat of a disaster. Let's dissect this a little bit:

- June 2022 has been the most popular month of June in Bixi's history
- I trained and tested my model with winter months included. I should test it without them to see if that has a positive impact (winter months have 0 users since the service is not offered.)
- I have only partial data for 2022. Everymonth of 2022 is beeting previous records.
- Years 2020 and 2021 were impacted by the health measures imposed by the Quebec government. Somehow reducing the weight of those years while training the model might lead to better results.

Overall I am quite happy with the outcome. This has been my first time using Python, pandas, seaborn, Jupyter notebooks, SQL, Google Big Query and beautiful Soup 4. I am definitely better prepared for the next project.

Thank you for reading! 😊