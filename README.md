# Powerlifting Data Science Project
**Goal:** To predict the squat, bench, and deadlift (DVs) of powerlifters
* Scraped ~10,000 powerlifting records and competition histories from 1000s of interconnected URLs using Selenium and BeautifulSoup
* Engineered 20 new columns, such as average competition sq/bn/dl, average rate of change in sq/bn/dl, and second best competition sq/bn/dl
* CatBoost encoded all categorical variables, and imputed nulls with MICE
* Optimized Multiple Linear Regression, Lasso, and Random Forest Regressor...
* Productionized...

## Resources
**Version:** Python 3.7
**Packages:** pandas, numpy, matplotlib, seaborn, sklearn, selenium, flask, pickle
**Flask Tutorial:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## Web Scraping
Using Selenium and BeautifulSoup, I scraped off data from openpowerlifting.org and the interconnected links to each powerlifter's competition history.

I created 26 columns:
* **Provided data:** *Federation, Date, Location, Sex, Age, Equip, Class, Weight, Squat, Bench, Deadlift, Total, Dots (score)*
* **Engineered from competition history:** *Squat/Bench/Deadlift averages across previous competitions, Squat/Bench/Deadlift averages of standard deviation across previous competitions across the best, Second best squat/bench/deadlift, Squat/Bench/Deadlift average rates of change across previous competitions, Count of competition history*

## Data Cleaning
* Dropped duplicate powerlifters
* Filled missing Class values by calculating from Weight
* Recoded columns types
* Imputed remaining nulls with MICE

## Feature Engineering
* CatBoost encoded all categorical variables
**Engineered 6 new columns:** Month, Season, Year, Country, State, Number of records in past year of the same class, Number of days since last record in the same class

## Exploratory Data Analysis
* Observed the distributions of continuous variables and the counts of categoricals
* Created scatterplots of each continuous variable against the DVs, as well as correlation dataframes
* Created box and violin plots of categorical variables against the DVs, as well as pivot tables
* Ran Kruskal-Wallis H-tests to observe if differences exist in the medians

**Some interesting takeaways (more included in file):**
* Surprisingly, age is a very weak predictor of squat/bench/deadlift (r<0.1)
* Strong predictors include weight, measures of one's powerlifting history, and one's current best squat/bench/deadlift (r>0.7). These support two conclusions:
  * Powerlifters are strong all-around and well-proportioned
  * The past reliably predicts the future

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/squat_avg_avg_against_squat.png)
![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/squat_corr.png)

* Wearing wraps boosts one's performance on squat, bench, and deadlift, as opposed to not wearing wraps.

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/wraps_against_squat.png) <!-- .element height="80%" width="80%" -->

* Some nationalities are much stronger on-average than others, and others are much weaker on-average than others. Crucially, these nationalities have very few competitors and are unlikely to be representative of the population (<5). With more competitors, we should expect a regression to the mean, and thus, smaller differences in strength between nationalities.

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/nationality_pivot.png) <!-- .element height="50%" width="50%" -->

## Model Building


## Productionizing

