from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from aldi import click, excluded_keyword_in
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
from csv import writer
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
import logging, json, os, sys, time, random
from selenium import webdriver

driver = webdriver.Chrome(executable_path="./chromedriver")
# driver = uc.Chrome(version_main=100)
# driver.maximize_window()
driver.get("https://www.pitstoparabia.com/")

nav_bar = driver.find_element(
    by=By.XPATH, value="//span[@id='responsive-nav-button-icon']"
)
nav_bar.click()
more = driver.find_element(by=By.XPATH, value="//span[@class='menu-button']")
more.click()
first = driver.find_element(by=By.XPATH, value="(//ul[@class='sub_menu'])[1]/li[1]")
first.click()
# //div[@class='popup']/div popup
