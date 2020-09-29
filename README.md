# Powerlifting Data Science Project
* Scraped ~10,000 powerlifting records and competition histories from 1000s of interconnected URLs using Selenium and BeautifulSoup
* Engineered 12 new columns, such as average competition sq/bn/dl, average rate of change in sq/bn/dl, and second best competition sq/bn/dl
* CatBoost encoded all categorical variables
* Optimized Multiple Linear Regression, Lasso, and Random Forest Regressor...
* Productionized...

## Technologies
**Packages:** pandas, numpy, matplotlib, seaborn, sklearn, selenium, flask, pickle


## Web Scraping
Using Selenium and BeautifulSoup, I scraped data off openpowerlifting.org and data from the associated links to each powerlifter's competition history. 

Please note: The reader may notice that openpowerlifting.org already provides a downloadable CSV file to save users time from scraping data. However, previous competition histories were in separate individual links. Believing that this data was helpful, I developed a web scraper that scraped the initial data, and then scraped the competition history in the attached links.

## Data Cleaning

## Feature Engineering

## Exploratory Data Analysis

## Model Building

## Productionizing

