# Powerlifting Data Science Project
**Goal:** To predict the best competition squat, bench, and deadlift (3 DVs) of powerlifters

**Product:** https://predicting-deadlift.herokuapp.com
* Scraped ~10,000 powerlifting records and competition histories from 1000s of interconnected URLs using Selenium and BeautifulSoup
* Engineered 20 new columns, such as average competition sq/bn/dl, average rate of change in sq/bn/dl, and second best competition sq/bn/dl
* CatBoost encoded all categorical variables, and imputed nulls with MICE
* Compared Multiple Linear Regression, Lasso, and Random Forest Regressors with MAE and RMSE (normalized to mean)
* Deployed Flask model (only for deadlift) to Heroku: https://predicting-deadlift.herokuapp.com

## Resources
* **Version:** Python 3.7
* **Packages:** pandas, numpy, matplotlib, seaborn, sklearn, selenium, flask, pickle
* **Flask and Heroku Tutorial:** https://blog.cambridgespark.com/deploying-a-machine-learning-model-to-the-web-725688b851c7

## Web Scraping
Using Selenium and BeautifulSoup, I scraped off data from openpowerlifting.org and the interconnected links to each powerlifter's competition history.

Out of the 31 columns, 24 were from available data:
* **11 Parsed from HTML:** *Federation, Date, Location, Sex, Age, Equip, Class, Weight, Squat, Bench, Deadlift*
* **13 Engineered from competition history:** 
  * Squat/Bench/Deadlift averages across previous competitions
  * Squat/Bench/Deadlift averages of standard deviation across previous competitions across the best
  * Second best squat/bench/deadlift
  * Squat/Bench/Deadlift average rates of change across previous competitions
  * Count of competition history

## Data Cleaning
* Dropped duplicate powerlifters
* Filled missing Class values by calculating from Weight
* Cleaned Age column and recast to int type
* Recast Date column to datetime object
* Recast Class column to string type
* Imputed remaining nulls with MICE

## Feature Engineering
* CatBoost encoded all categorical variables
* **Created 7 new columns:**
  * Parsed Date column into Month, Season, and Year columns
  * Parsed Location column into Country and State columns
  * Created column for Number of records in the past year of the same Class
  * Created column for Number of days since the last record in the same Class

## Exploratory Data Analysis
* Observed the distributions of continuous variables and the counts of categoricals
* Created correlation dataframes and scatterplots of each continuous variable against the DVs
* Created pivot tables and box and violin plots of categorical variables against the DVs
* Ran Kruskal-Wallis H-tests to observe if differences exist in the medians

**Some interesting takeaways (more included in file):**
* Average squat, bench, and deadlift are 597.7 lbs, 381.4 lbs, and 626.1 lbs respectively
* Surprisingly, age is a very weak predictor of squat/bench/deadlift (r<0.1)
* Strong predictors include weight, measures of one's powerlifting history, and one's current best squat/bench/deadlift (r>0.7). These support two conclusions:
  * Past performance reliably predicts future performance
  * Powerlifters are strong all-around and likely have well-proportioned physiques (as squat/bench/deadlift work out most muscle groups)

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/squat_avg_avg_against_squat.png) <!-- .element height="20%" width="20%" -->
![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/squat_corr.png) <!-- .element height="20%" width="20%" -->

* Wearing wraps boosts one's performance on squat, bench, and deadlift, as opposed to not wearing wraps (p<0.01).

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/wraps_against_squat.png) <!-- .element height="30%" width="30%" -->

* Some nationalities are much stronger on-average than others, and others are much weaker on-average than others. Crucially, these nationalities have very few competitors and are unlikely to be representative of the population (<5). With more competitors, we should expect a regression to the mean, and thus, smaller differences in strength between nationalities.

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/nationality_pivot.png) <!-- .element height="50%" width="50%" -->

## Model Building
After CatBoost encoding the models, I split the data into train and test sets of 80% to 20%. I compared three regression algorithms, one for each DV, for a total of 9 models:

* **Linear:** Baseline model
* **Lasso:** A method that reduces the coefficients of each variable to zero relative to their prediction error (i.e. importance) via regularization, which reduces overfitting
* **Random Forest:** Broadly, a combination of decision trees whose outputs are averaged to provide a single output

**Evaluation Metrics:**
I retrieved the MAE, RMSE, and normalized RMSE (RMSE/mean of DV) of each model:
* **Squat:** mean=597.7 lbs, stdev=123.5 lbs
  * Linear: MAE=30.5, RMSE=41.8, nRMSE=0.0699
  * Lasso: MAE=30.5, RMSE=41.5, nRMSE=0.0694
  * Random Forest: MAE=24.1, RMSE=35.1, nRMSE=0.0587
* **Bench:** mean=381.4 lbs, stdev=87.4 lbs
  * Linear: MAE=16.8, RMSE=23.6, nRMSE=0.0618
  * Lasso: MAE=16.8, RMSE=23.6, nRMSE=0.0618
  * Random Forest: MAE=15.3, RMSE=21.9, nRMSE=0.0574
* **Deadlift:** mean=626.1 lbs, stdev=103.3
  * Linear: MAE=16.4, RMSE=22.6, nRMSE=0.0360
  * Lasso: MAE=16.5, RMSE=22.6, nRMSE=0.0360
  * Random Forest: MAE=16.7, RMSE=22.5, nRMSE=0.0359

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/model_performance_squat.png) <!-- .element height="100%" width="100%" -->

## Productionizing
Using the following article (https://blog.cambridgespark.com/deploying-a-machine-learning-model-to-the-web-725688b851c7), I deployed a flask-wrapped random forest regressor model to heroku here: https://predicting-deadlift.herokuapp.com

## Further Improvments
"All models are wrong, but some are useful." And many are in need of improvement!

As I continue to learn more optimization techniques, I recognize the ways I could have reduced the RMSE even further:
* Add a cross-validation set
* Scrape more data
* Use SelectKBest to choose the most important features and minimize data required from users
* Use GridsearchCV to optimize model hyperparameters, in addition to the model parameters
* Use ensemble methods
* Remove outliers
* Try using PCA
* Impute the DVs to add around 1% more rows of data
