# Powerlifting Data Science Project
**Goal:** To predict the best competition squat, bench, and deadlift (3 DVs) of powerlifters

**Significance:** Imagine you are betting on who will score the highest in a given competition. This product can tell you the squat, bench, and deadlift (which can then be calculated into a competition score) of a powerlifter with fairly good reliability.

**Product:** https://predicting-deadlift.herokuapp.com
* Scraped ~10,000 powerlifting records and competition histories from 1000s of interconnected URLs using Selenium and BeautifulSoup
* Engineered 20 new columns, such as average competition sq/bn/dl, average rate of change in sq/bn/dl, and second best competition sq/bn/dl
* CatBoost encoded all categorical variables, and imputed nulls with MICE
* Compared Multiple Linear Regression, Lasso, and Random Forest Regressors with MAE and RMSE (normalized to mean)
* Deployed Flask model (only for deadlift) to Heroku: https://predicting-deadlift.herokuapp.com

## 1. Resources
* **Version:** Python 3.7
* **Packages:** pandas, numpy, matplotlib, seaborn, sklearn, selenium, flask, pickle
* **Flask and Heroku Tutorial:** https://blog.cambridgespark.com/deploying-a-machine-learning-model-to-the-web-725688b851c7

## 2. Web Scraping
Using Selenium and BeautifulSoup, I scraped off data from openpowerlifting.org and the interconnected links to each powerlifter's competition history.

Out of the 31 columns, 24 were from available data:
* **11 Parsed from HTML:** *Federation, Date, Location, Sex, Age, Equip, Class, Weight, Squat, Bench, Deadlift*
* **13 Engineered from competition history:** 
  * Squat/Bench/Deadlift averages across previous competitions
  * Squat/Bench/Deadlift averages of standard deviation across previous competitions across the best
  * Second best squat/bench/deadlift
  * Squat/Bench/Deadlift average rates of change across previous competitions
  * Count of competition history

## 3. Data Cleaning
* Dropped duplicate powerlifters
* Filled missing Class values by calculating from Weight
* Cleaned Age column and recast to int type
* Recast Date column to datetime object
* Recast Class column to string type
* Imputed remaining nulls with MICE

## 4. Feature Engineering
* CatBoost encoded all categorical variables
* **Created 7 new columns:**
  * Parsed Date column into Month, Season, and Year columns
  * Parsed Location column into Country and State columns
  * Created column for Number of records in the past year of the same Class
  * Created column for Number of days since the last record in the same Class

## 5. Exploratory Data Analysis
* Observed the distributions of continuous variables and the counts of categoricals
* Created correlation dataframes and scatterplots of each continuous variable against the DVs
* Created pivot tables and box and violin plots of categorical variables against the DVs
* Ran Kruskal-Wallis H-tests to observe if differences exist in the medians

**Some interesting takeaways (more included in file):**
* **Powerlifters are really strong** 
  * The average squat, bench, and deadlift are 597.7 lbs, 381.4 lbs, and 626.1 lbs respectively
* **You can be strong at any age** 
  * Surprisingly, age is a very weak predictor of squat/bench/deadlift (r<0.1)
* **Past performance reliably predicts future performance; powerlifters are *all-around* strong; and they are likely well-proportioned physically** 
  * Strong predictors include weight, measures of one's powerlifting history, and one's current best squat/bench/deadlift (r>0.7)

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/squat_avg_avg_against_squat.png) <!-- .element height="20%" width="20%" -->
![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/squat_corr.png) <!-- .element height="20%" width="20%" -->

* **You should wear wraps to lift more**
  * Wearing wraps boosts one's performance on squat, bench, and deadlift, as opposed to not wearing wraps (p<0.01).

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/wraps_against_squat.png) <!-- .element height="30%" width="30%" -->

* **Some nationalities are much stronger on-average than others, particularly Eastern Europeans. But...** 
  * Note that these nationalities have very few competitors and are thus unlikely to be representative of the population (<5). With larger samples, we should expect a regression to the mean and smaller disparities in strength. Until we obtain larger samples, we don't know much smaller the disparity, but we should assume *some* reduction in the disparity.

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/nationality_pivot.png) <!-- .element height="50%" width="50%" -->

## 6. Model Building
After CatBoost encoding the models, I split the data into train and test sets of 80% to 20%. I compared 3 regression algorithms, 1 for each of the 3 DV's, for a total of 9 models:

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
* **Deadlift:** mean=626.1 lbs, stdev=103.3 lbs
  * Linear: MAE=16.4, RMSE=22.6, nRMSE=0.0360
  * Lasso: MAE=16.5, RMSE=22.6, nRMSE=0.0360
  * Random Forest: MAE=16.7, RMSE=22.5, nRMSE=0.0359

The normalized RMSE results show that, on average, the error of the predictions are 3% to 6% of the mean weights. This does not mean 3% to 6% error in *accuracy* (which we could calculate by averging the percentage of each absolute difference between prediction and actual), and this does not tell us the *variability* of the error (which we could peek into by calculating the nRMSEs from the mean plus/minus 2 standard deviations). We, however, learn that overall the models are not at all far off in predicting the bests of an aggregate of powerlifters, and in particular, we see that the random forest regressors perform the best across all three DV's.

![alt text](https://github.com/andrewjlee0/powerlifting/blob/master/images/model_performance_squat.png) <!-- .element height="100%" width="100%" -->

## 7. Productionizing
Using the following article (https://blog.cambridgespark.com/deploying-a-machine-learning-model-to-the-web-725688b851c7), I deployed a flask-wrapped random forest regressor model to heroku: https://predicting-deadlift.herokuapp.com

## 8. Further Improvments
"All models are wrong, but some are useful." And many are in need of improvement!

As I continue to learn best practices, I recognize the ways I could have reduced the RMSE even further:
* Add a cross-validation set
* Scrape more data
* Use SelectKBest to choose the most important features and minimize data required from users
* Use GridsearchCV to optimize model hyperparameters, in addition to the model parameters
* Use ensemble methods
* Remove outliers
* Try using PCA
* Impute the DVs to add around 1% more rows of data
