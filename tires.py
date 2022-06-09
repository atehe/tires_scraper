from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
from csv import writer
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
import logging, json, os, sys, time, random
from selenium import webdriver

# driver = uc.Chrome(version_main=100)
driver = webdriver.Chrome(executable_path="./chromedriver")

driver.maximize_window()


def clean_rimsize_attribute(text):
    last_index = text[::-1].index(")")
    first_index = text[::-1].index(",")
    return text[-first_index:-1].strip("'")


def action_click(driver, button):
    action = ActionChains(driver)
    action.move_to_element(to_element=button)
    action.click()
    action.perform()


def handle_popup(driver):
    try:
        close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='exit_popup_container']//div[contains(@class, 'close')]/a",
                )
            )
        )
        close.click()
    except:
        print("handled")


driver.get(
    "https://www.pitstoparabia.com/en/advancesearch?dir=asc&form_key=ZhnnkEn2CKFHEVxX&width=221&height=19&rim_size=235&rear_width=&rear_height=&rear_rim_size=&sizelocation=Dubai"
)


def load_all_tires(driver):
    tires_loaded = driver.find_elements(
        by=By.XPATH, value="//div[@id='all-grid']//li/div"
    )
    num_tires = driver.find_element(by=By.XPATH, value="//span[@id='number_count']")


def click(element, driver):
    """Use javascript click if selenium click method fails"""
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)


def select_n_close(element, driver):
    """Selects value from filter popup and closes"""
    click(element, driver)
    text = element.find_element(
        by=By.XPATH, value="./a"
    ).text or clean_rimsize_attribute(
        element.find_element(by=By.XPATH, value="./a").get_attribute("onclick")
    )

    close = driver.find_element(
        by=By.XPATH,
        value="//div[@class='modal' and @style='display: block;']//span[@class='close']",
    )
    click(close, driver)
    time.sleep(1)
    return text


def width_options(driver):
    try:
        width_button = driver.find_element(
            by=By.XPATH, value="//input[@id='widthvalue']/preceding-sibling::a"
        )

        width_button.click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
                )
            )
        )
    except:
        popup_close = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='exit_popup_container']//div[contains(@class, 'close')]/a",
                )
            )
        )
        click(popup_close, driver)
        width_options(driver)

    widths = driver.find_elements(
        by=By.XPATH,
        value="//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
    )
    return widths


def height_options(driver):
    try:
        height_button = driver.find_element(
            by=By.XPATH, value="//input[@id='heightvalue']/preceding-sibling::a"
        )
        click(height_button, driver)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//ul[@id='height']//li",
                )
            )
        )
    except:
        popup_close = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='exit_popup_container']//div[contains(@class, 'close')]/a",
                )
            )
        )
        click(popup_close, driver)
        height_options(driver)

    heights = driver.find_elements(by=By.XPATH, value="//ul[@id='height']//li")
    return heights


def rim_options(driver):
    try:
        rimsize_button = driver.find_element(
            by=By.XPATH, value="//input[@id='rimsizevalue']/preceding-sibling::a"
        )
        click(rimsize_button, driver)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//ul[@id='rimsize']//li",
                )
            )
        )
    except:
        popup_close = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='exit_popup_container']//div[contains(@class, 'close')]/a",
                )
            )
        )
        click(popup_close, driver)
        rim_options(driver)
    rims = driver.find_elements(by=By.XPATH, value="//ul[@id='rimsize']//li")
    return rims


def parse_tire_sizes(driver):

    with open("search_urls.csv", "a") as url, open("tires.txt", "a") as tires:
        search_writer = writer(url)
        search_writer.writerow(("width", "height", "rimsize", "search url"))

        while True:
            refine_result_bar = driver.find_element(
                by=By.XPATH, value="//div[@id='accordion_refine_result']"
            )
            click(refine_result_bar, driver)
            time.sleep(1)

            widths = width_options(driver)
            for w, width in enumerate(widths):
                width_selected = select_n_close(widths[w], driver)

                heights = height_options(driver)
                for h, height in enumerate(heights):
                    height_selected = select_n_close(heights[h], driver)

                    rims = rim_options(driver)
                    for r, rim in enumerate(rims):

                        rim_selected = select_n_close(rims[r], driver)

                        print(
                            f"selected: {(width_selected, height_selected, rim_selected)}"
                        )
                        search = driver.find_element(
                            by=By.XPATH, value="//button[@id='submitbtnresponsive']"
                        )
                        click(search, driver)
                        time.sleep(3)
                        current_url = driver.current_url
                        search_writer.writerow(
                            (width_selected, height_selected, rim_selected, current_url)
                        )
                        refine_result_bar = driver.find_element(
                            by=By.XPATH, value="//div[@id='accordion_refine_result']"
                        )
                        click(refine_result_bar, driver)

                        # update elements that will be selected from in the loop
                        if r < len(rims) - 1:
                            rims = rim_options(driver)
                    if h < len(heights) - 1:
                        heights = height_options(driver)
                if w < len(widths) - 1:
                    widths = width_options(driver)


parse_tire_sizes(driver)
