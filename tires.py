from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# from aldi import click, excluded_keyword_in
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
from csv import writer
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
import logging, json, os, sys, time, random

driver = uc.Chrome(version_main=100)
driver.maximize_window()
# driver.get("https://www.pitstoparabia.com/")

# refine_result_bar = find_element(
#     by=By.XPATH, value="//div[@id='accordion_refine_result']"
# )


# width_button = driver.find_element(by=By.XPATH, value="//input[@id='widthvalue']")
# height_button = driver.find_element(by=By.XPATH, value="//input[@id='heightvalue']")
# rimsize_button = driver.find_element(by=By.XPATH, value="//input[@id='rimsizevalue']")
# submit_button = driver.find_element(
#     by=By.XPATH,
#     value="//div[@id='sizelocation_popup' and @style='display: block;']//div[@class='input_field']/following-sibling::button",
# )
# location_bar = driver.find_element(
#     by=By.XPATH,
#     value="//div[@id='sizelocation_popup' and @style='display: block;']//div[@class='input_field']",
# )


# width_selection_choice = driver.find_elements(
#     by=By.XPATH,
#     value="//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
# )

# rimsize_selection_choice = driver.find_element(
#     by=By.XPATH, value="//ul[@id='rimsize']//li"
# )
# height_selection_choice = driver.find_element(
#     by=By.XPATH, value="//ul[@id='rimsize']//li"
# )
# back_button = driver.find_element(
#     by=By.XPATH,
#     value="//div[@id='myModal' and @style='display: block;']//div[@class='back_to_prev']",
# )
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


# driver.get(
#     "https://www.pitstoparabia.com/en/advancesearch?dir=asc&form_key=ZhnnkEn2CKFHEVxX&width=221&height=19&rim_size=235&rear_width=&rear_height=&rear_rim_size=&sizelocation=Dubai"
# )
# handle_popup(driver)

# while True:
#     refine_result_bar = driver.find_element(
#         by=By.XPATH, value="//div[@id='accordion_refine_result']"
#     )
#     refine_result_bar.click()
#     time.sleep(2)
#     width_button = driver.find_element(
#         by=By.XPATH, value="//input[@id='widthvalue']/preceding-sibling::a"
#     )
#     # action_click(driver, width_button)
#     width_button.click()
#     print("width clicked")
#     time.sleep(2)
#     width_selection_choice = driver.find_elements(
#         by=By.XPATH,
#         value="//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
#     )
#     for width in width_selection_choice:
#         width.click()
#         widthsize = width.text
#         time.sleep(3)

#         height_selection_choice = driver.find_elements(
#             by=By.XPATH, value="//ul[@id='height']//li"
#         )
#         for height in height_selection_choice:
#             height.click()
#             heightsize = height.text
#             time.sleep(3)
#             rimsize_selection_choice = driver.find_elements(
#                 by=By.XPATH, value="//ul[@id='rimsize']//li"
#             )
#             for rim in rimsize_selection_choice:
#                 rim.click()
#                 rimsize = rim.text
#                 time.sleep(3)
#                 location_bar = driver.find_element(
#                     by=By.XPATH,
#                     value="//div[@id='sizelocation_popup' and @style='display: block;']//div[@class='input_field']/input",
#                 )
#                 location_bar.clear()
#                 location_bar.send_keys("dubai" + Keys.RETURN)
#                 submit_button = driver.find_element(
#                     by=By.XPATH,
#                     value="//div[@id='sizelocation_popup' and @style='display: block;']//div[@class='input_field']/following-sibling::button",
#                 )
#                 submit_button.click()
#                 print(f"selected: {(widthsize, heightsize, rimsize)}")

#                 rimsize_button = driver.find_element(
#                     by=By.XPATH, value="//input[@id='rimsizevalue']"
#                 )
#                 rimsize_button.click()

#                 rimsize_selection_choice = driver.find_elements(
#                     by=By.XPATH, value="//ul[@id='rimsize']//li"
#                 )


driver.get(
    "https://www.pitstoparabia.com/en/advancesearch?dir=asc&form_key=ZhnnkEn2CKFHEVxX&width=221&height=19&rim_size=235&rear_width=&rear_height=&rear_rim_size=&sizelocation=Dubai"
)
handle_popup(driver)

while True:
    refine_result_bar = driver.find_element(
        by=By.XPATH, value="//div[@id='accordion_refine_result']"
    )
    refine_result_bar.click()
    time.sleep(2)
    width_button = driver.find_element(
        by=By.XPATH, value="//input[@id='widthvalue']/preceding-sibling::a"
    )
    # action_click(driver, width_button)
    width_button.click()
    print("width clicked")
    time.sleep(2)
    width_selection_choice = driver.find_elements(
        by=By.XPATH,
        value="//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
    )
    for w, width in enumerate(width_selection_choice):
        width_selection_choice[w].click()
        widthsize = width_selection_choice[w].text
        time.sleep(3)

        close = driver.find_element(
            by=By.XPATH,
            value="//div[@id='myModal' and @style='display: block;']//div[@class='back_to_prev']/following-sibling::span",
        )
        close.click()
        time.sleep(2)
        # selct heigh button
        height_button = driver.find_element(
            by=By.XPATH, value="//input[@id='heightvalue']/preceding-sibling::a"
        )
        height_button.click()
        time.sleep(2)
        # select  all height options
        height_selection_choice = driver.find_elements(
            by=By.XPATH, value="//ul[@id='height']//li"
        )
        for h, height in enumerate(height_selection_choice):
            # click from height options
            height_selection_choice[h].click()
            heightsize = height_selection_choice[h].text
            time.sleep(3)

            close = driver.find_element(
                by=By.XPATH,
                value="//div[@id='myModal' and @style='display: block;']//div[@class='back_to_prev']/following-sibling::span",
            )
            close.click()

            rimsize_button = driver.find_element(
                by=By.XPATH, value="//input[@id='rimsizevalue']/preceding-sibling::a"
            )
            rimsize_button.click()
            time.sleep(2)
            rimsize_selection_choice = driver.find_elements(
                by=By.XPATH, value="//ul[@id='rimsize']//li"
            )
            for r, rim in enumerate(rimsize_selection_choice):
                rimsize_selection_choice[r].click()
                rimsize = rimsize_selection_choice[r].text
                time.sleep(2)
                close = driver.find_element(
                    by=By.XPATH,
                    value="//div[@id='sizelocation_popup' and @style='display: block;']//div[@class='back_to_prev']/following-sibling::span",
                )
                close.click()
                # time.sleep(3)
                # location_bar = driver.find_element(
                #     by=By.XPATH,
                #     value="//div[@id='sizelocation_popup' and @style='display: block;']//div[@class='input_field']/input",
                # )
                # location_bar.clear()
                # location_bar.send_keys("dubai" + Keys.RETURN)
                # submit_button = driver.find_element(
                #     by=By.XPATH,
                #     value="//div[@id='sizelocation_popup' and @style='display: block;']//div[@class='input_field']/following-sibling::button",
                # )
                # submit_button.click()
                print(f"selected: {(widthsize, heightsize, rimsize)}")

                # rimsize_button = driver.find_element(
                #     by=By.XPATH, value="//input[@id='rimsizevalue']"
                # )
                # rimsize_button.click()

                # rimsize_selection_choice = driver.find_elements(
                #     by=By.XPATH, value="//ul[@id='rimsize']//li"
                # )
                if r < len(rimsize_selection_choice) - 1:
                    rimsize_button = driver.find_element(
                        by=By.XPATH,
                        value="//input[@id='rimsizevalue']/preceding-sibling::a",
                    )
                    rimsize_button.click()
                    time.sleep(2)
                    rimsize_selection_choice = driver.find_elements(
                        by=By.XPATH, value="//ul[@id='rimsize']//li"
                    )
            if h < len(height_selection_choice) - 1:
                height_button = driver.find_element(
                    by=By.XPATH, value="//input[@id='heightvalue']/preceding-sibling::a"
                )
                height_button.click()
                time.sleep(2)
                height_selection_choice = driver.find_elements(
                    by=By.XPATH, value="//ul[@id='height']//li"
                )
        if w < len(width_selection_choice) - 1:
            width_button = driver.find_element(
                by=By.XPATH, value="//input[@id='widthvalue']/preceding-sibling::a"
            )
            width_button.click()
            time.sleep(2)
            width_selection_choice = driver.find_elements(
                by=By.XPATH,
                value="//div[@id='myModal' and @style='display: block;']//div[@class='filter_values']//li",
            )
