#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 16:10:29 2020

@author: andrew
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import numpy as np
import pandas as pd

def get_info(lifter):
    # Get all provided info
    lifter_info = []
    for i in range(1,16):
        col_val = lifter.find('div', class_='slick-cell l{i} r{i}'.format(i=i))
        if i in (2,4):
            col_val = col_val.find('a')
        if i in (11,12,13):
            col_val = col_val.find('span')
        lifter_info.append(col_val.text)

    # Since previous competition history is also linked, we will account for it
    URL_previous_comps = URL + lifter.find('div', class_='slick-cell l2 r2').find('a')['href']
    driver.execute_script('''window.open("{}","_blank");'''.format(URL_previous_comps))
    driver.switch_to.window(window_name = driver.window_handles[-1])
    html = driver.execute_script("return document.getElementsByTagName('table')[1].innerHTML")
    soup = BeautifulSoup(html, 'html.parser')
    previous_comps = soup.find('tbody').find_all('tr')

    # Create new dataframe to store previous competition history
    sq_cols = ['squat1','squat2','squat3','squat4']
    bn_cols = ['bench1','bench2','bench3','bench4']
    dl_cols = ['dl1','dl2','dl3','dl4']
    cols = ['date'] + sq_cols + bn_cols + dl_cols
    previous_comps_df = pd.DataFrame(columns = cols)

    # Populate dataframe
    previous_comps_idx = 0
    for comp in previous_comps:
        comp_info = comp.find_all('td')
        row = []
        counts = {'squat':0, 'bench':0, 'deadlift':0}
        for i in range(len(comp_info)):

            # Only append squat, bench, dl, dots, and datetime col vals
            class_ = comp_info[i].get('class')
            class_ = class_[0] if class_ != None else class_
            if (class_ not in counts) and (i != 2):
                continue
            row.append(comp_info[i].text)

            # Add np.nans to row if missing squat, bench, or dl info in comp_info
            if class_ in counts:
                counts[class_] += 1
                next_class = comp_info[i+1].get('class')
                next_class = next_class[0] if next_class != None else next_class
                if class_ != next_class:
                    num_nans = 4 - counts[class_]
                    for n in range(num_nans):
                        row.append(np.nan)
        try:
            previous_comps_df.loc[previous_comps_idx] = row
            previous_comps_idx += 1
        except:
            name = lifter.find('div', class_='slick-cell l2 r2').find('a')
            print('failed to append previous competition history of ', name.text)

    previous_comps_df = previous_comps_df.replace(r'^\s*$', np.nan, regex=True)

    for cols in (sq_cols, bn_cols, dl_cols):
        # Convert str to float, and even if score is not valid (negative symbol), absolute value it
        previous_comps_df[cols] = previous_comps_df[cols].astype(float).abs()

        # Get value and location of best weight in cols, and remove it from averaging
        best = previous_comps_df[cols].max().max()
        i, c = np.where(previous_comps_df == best)
        if len(i) > 0 and len(c) > 0:
            previous_comps_df.iat[i[0], c[0]] = np.nan

        # To account for previous history, get average of averages of squat, bench, and dl
        avg = previous_comps_df[cols].mean(axis = 1)

        # Average rate of change/improvement over the past (at most) 5 recent competitions
        # The number choice is arbitrary
        difference = avg - avg.shift(1)
        avg_rate_change = difference.mean()

        # Average of averages, and standard deviations, excluding the best performance
        avg_avg = avg.mean()
        avg_std = avg.std()

        # Second best squat/bench/dl from a competition other than their best
        # If only been to one comp, then no second_best, and will impute later in data cleaning
        largest_two = avg.nlargest(2)
        second_best = np.nan if pd.isna(best) or len(largest_two) == 0 else largest_two.iloc[0]

        lifter_info += [avg_avg, avg_std, second_best, avg_rate_change]

    # Total number of previous comps attended
    comp_count = len(previous_comps_df.index)
    lifter_info.append(comp_count)

    # print(len(lifter_info))
    # print(lifter_info)
    # print('--------------------------------------')

    driver.close()
    driver.switch_to.window(window_name = driver.window_handles[0])
    return lifter_info

########################################################################################################################

URL = 'https://www.openpowerlifting.org'

# Open URL with Selenium driver
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get(URL)

# Create CSV file
output = '/Users/andrew/OneDrive - Williams College/Data Science Projects/Independent/powerlifting'
with open(output + '/web_scraper_output.csv', 'w') as fw:
    writer = csv.writer(fw, delimiter=',')

    num_scrolldowns = 250
    for i in range(num_scrolldowns):
        # Make sure on driver is viewing rankings URL page, and scroll down
        driver.switch_to.window(window_name = driver.window_handles[0])
        element = "document.getElementsByClassName('slick-viewport slick-viewport-top slick-viewport-left')[0]"
        driver.execute_script("{e}.scrollTop = {px}".format(e=element, px=1100*i))

        # Create two BeautifulSoups, since there are two CSS classes in separate div elements
        html = driver.execute_script("return document.getElementById('theGrid').innerHTML")
        soup = BeautifulSoup(html, 'html.parser').find(class_='grid-canvas grid-canvas-top grid-canvas-left')
        rankings_even = soup.find_all('div', class_='ui-widget-content slick-row even')
        rankings_odd = soup.find_all('div', class_='ui-widget-content slick-row odd')

        # Parse the data in each BeautifulSoup
        for rankings in (rankings_even, rankings_odd):
            for lifter in rankings:
                lifter_info = get_info(lifter)
                if len(lifter_info) == 28:
                    writer.writerow(lifter_info)
        fw.flush()
driver.quit()
