from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pandas as pd
from bs4 import BeautifulSoup

def get_tsx_filtered():
    driver = webdriver.Chrome('A:/Projects/Ultimate Trader/chromedriver.exe')

    driver.get(
        'https://www.barchart.com/ca/stocks/stocks-screener?screener=222218&viewName=main')

    login_button = driver.find_element(
        By.XPATH, '/html/body/main/div/div[1]/div[2]/div/div/div[2]/div[1]/a[1]').click()
        #/html/body/main/div/div[1]/div[2]/div/div/div[2]/div[1]/a[1]

    username = 'egf92755@jiooq.com'
    password = 'killinit'
    
    time.sleep(5)
    username_field = driver.find_element(
        By.XPATH, '//*[@id="bc-login-form"]/div[1]/input')

    username_field.clear()
    username_field.send_keys(username)
    time.sleep(2)
    password_field = driver.find_element(By.CSS_SELECTOR, '#login-form-password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # this wait time is necessary so the site loads all available options before selecting them
    time.sleep(5)

    select_screener = Select(driver.find_element(By.CSS_SELECTOR, '#main-content-column > div > div.bc-screener.ng-isolate-scope > div:nth-child(2) > div > screener-load-screener-toolbar > div > screener-saved-screeners > div > select'))
    # this is the value of the saved screener "relative volume"
    select_screener.select_by_value('object:15')

    see_results_button = driver.find_element(By.CSS_SELECTOR, '#main-content-column > div > div.bc-screener.ng-isolate-scope > div:nth-child(2) > div > div.bc-screener__submit-button > a').click()
    #main-content-column > div > div.bc-screener.ng-isolate-scope > div:nth-child(2) > div > div.bc-screener__submit-button > a


    output_lst = []
    time.sleep(3)


    shadow_host_parent = driver.find_element(By.XPATH, '//*[@id="main-content-column"]/div/div[3]/div[3]/div[4]/div[2]')

    shadow_host = shadow_host_parent.find_element(By.TAG_NAME,'bc-data-grid')

    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_elements(By.CSS_SELECTOR, '#_grid')

    print(shadow_content)

    for row in shadow_content:
        cols = row.find_elements(By.XPATH, ".//*[contains(@class,'_cell')]")
        output_lst = [col.text for col in cols]

    list = output_lst


    start_count = 0
    end_count = 10 
    indent_list = end_count# this is the number of columns that need to be added (inluding the empty columns)
    print(len(list))
    rows = int(len(list)/end_count)
    print(rows)


    for i in range(rows):
        if start_count == 0:
            new_list = [list[start_count:end_count]]
        else:
            new_list.append(list[start_count:end_count])

        start_count = end_count
        end_count = end_count + 10

    print(new_list)
    df = pd.DataFrame(new_list[1:], columns=new_list[0])
    market_cap_col = df['Market Cap, $K'].replace(',','',regex=True).astype(int)
    df['Market Cap, $K'] = market_cap_col
    df.to_csv('tsx_filtered.csv')
