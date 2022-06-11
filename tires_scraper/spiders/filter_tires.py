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


logging.basicConfig(level=logging.INFO)


def extract_num(text):
    int_text = ""
    for char in text:
        if char.isalnum():
            int_text += char
    return int(int_text)


def clean_rimsize_attribute(text):
    last_index = text[::-1].index(")")
    first_index = text[::-1].index(",")
    return text[-first_index:-1].strip("'")


def click(element, driver):
    """Use javascript click if selenium click method fails"""
    try:

        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)


def select_n_close(element, driver):
    """Selects and returns a value from filter popup then closes it"""
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
    width_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[@id='widthvalue']/preceding-sibling::a",
            )
        )
    )
    click(width_button, driver)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
            )
        )
    )

    widths = driver.find_elements(
        by=By.XPATH,
        value="//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
    )
    return widths


def height_options(driver):
    height_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[@id='heightvalue']/preceding-sibling::a",
            )
        )
    )

    click(height_button, driver)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//ul[@id='height']//li",
            )
        )
    )
    heights = driver.find_elements(by=By.XPATH, value="//ul[@id='height']//li")
    return heights


def rim_options(driver):
    rimsize_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//input[@id='rimsizevalue']/preceding-sibling::a",
            )
        )
    )
    click(rimsize_button, driver)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//ul[@id='rimsize']//li",
            )
        )
    )

    rims = driver.find_elements(by=By.XPATH, value="//ul[@id='rimsize']//li")
    return rims


def parse_filters(driver, output_csv):
    output_csv = f"./utils/{output_csv}"
    with open(output_csv, "a") as tires:
        tire_writer = writer(tires)
        tire_writer.writerow(("width", "height", "rimsize", "tire url"))

        while True:
            refine_result_bar = driver.find_element(
                by=By.XPATH, value="//div[@id='accordion_refine_result']"
            )
            click(refine_result_bar, driver)

            widths = width_options(driver)[12:]
            for w, width in enumerate(widths):
                width_selected = select_n_close(widths[w], driver)

                heights = height_options(driver)
                for h, height in enumerate(heights):
                    height_selected = select_n_close(heights[h], driver)

                    rims = rim_options(driver)
                    for r, rim in enumerate(rims):

                        rim_selected = select_n_close(rims[r], driver)

                        search = driver.find_element(
                            by=By.XPATH, value="//button[@id='submitbtnresponsive']"
                        )
                        click(search, driver)
                        logging.info(
                            f">>> Filter: {(width_selected, height_selected, rim_selected)}"
                        )

                        load_all_tires(driver)

                        parse_filter_result(
                            driver,
                            tire_writer,
                            width_selected,
                            height_selected,
                            rim_selected,
                        )
                        if (
                            r == len(rims) - 1
                            and h == len(heights) - 1
                            and w == len(widths) - 1
                        ):
                            break

                        refine_result_bar = driver.find_element(
                            by=By.XPATH, value="//div[@id='accordion_refine_result']"
                        )
                        click(refine_result_bar, driver)

                        # update driver elements to be selected next
                        if r < len(rims) - 1:
                            rims = rim_options(driver)

                    if h < len(heights) - 1:
                        heights = height_options(driver)
                if w < len(widths) - 1:
                    widths = width_options(driver)[12:]


def load_all_tires(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@id='all-grid']//li/div",
                )
            )
        )
    except:
        return None

    tires_loaded = driver.find_elements(
        by=By.XPATH, value="//div[@id='all-grid']//li/div"
    )
    num_tires = driver.find_element(
        by=By.XPATH, value="//span[@id='number_count']"
    ).text
    load_count = 0
    while len(tires_loaded) < extract_num(num_tires):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_count += 1

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@id='loadingmask2' and @style='display: none;']",
                )
            )
        )
        tires_loaded = driver.find_elements(
            by=By.XPATH, value="//div[@id='all-grid']//li/div"
        )
    logging.info(">>> All Tires loaded")
    time.sleep(1)

    if load_count > 1:
        # multiple strategies to ensure driver returns
        # to top of the page(to prevent bot crash)
        try:
            refine_result_bar = driver.find_element(
                by=By.XPATH, value="//div[@id='accordion_refine_result']"
            )
            action = ActionChains(driver)
            action.move_to_element(to_element=refine_result_bar)
            action.perform()
        except:
            try:
                top = driver.find_element(
                    by=By.XPATH, value="(//div[@class='top_section'])[1]"
                )
                action = ActionChains(driver)
                action.move_to_element(to_element=top)
                action.perform()
            except:
                driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")


def parse_filter_result(driver, csv_writer, width, height, rimsize):
    page_response = Selector(text=driver.page_source.encode("utf8"))

    tires = page_response.xpath("//div[@id='all-grid']//li/div")
    for tire in tires:
        url = tire.xpath(".//a[@class='prod_thumbnail']/@href").get()
        if not url.startswith("http"):
            url = url.strip("/")
            url = f"https://www.pitstoparabia.com/{url}"
        csv_writer.writerow((width, height, rimsize, url))
    logging.info(f">>> Tires for {width}, {height}, {rimsize} extracted successfully")


def extract_filename(url, **kwargs):
    if url:

        url = url.strip("/")
        last_slash_index = url[::-1].index("/")
        return url[-last_slash_index:]
