import scrapy, os
from tires_scraper.spiders.filter_tires import *
from scrapy_selenium import SeleniumRequest
import pandas as pd
import urllib.request


def get_tyre_category(tyre_type):
    if tyre_type:
        if "SUV MT" in tyre_type or "SUV AT" in tyre_type:
            return "Off Road Tyres"
        if "Car" in tyre_type:
            return "Car Tyres"
        if "SUV" in tyre_type:
            return "SUV Tyres"
        if "Commercial" in tyre_type:
            return "Commercial Tyres"


def download_image(url, filename):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [
            (
                "User-Agent",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36",
            )
        ]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, f"./utils/{filename}")
    except:
        logging.error(f">>> {filename} couldn't be downloaded")


class PitstoparabiaSpider(scrapy.Spider):
    name = "pitstoparabia"
    allowed_domains = ["www.pitstoparabia.com"]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.pitstoparabia.com/en/advancesearch?dir=asc&form_key=YTop2Giq9qdZ8Ke2&width=221&height=19&rim_size=235&rear_width=&rear_height=&rear_rim_size=&sizelocation=Dubai",
            callback=self.tires_to_csv,
        )

    def tires_to_csv(self, response):
        driver = response.meta["driver"]

        try:
            parse_filters(driver, "./utils/all_tires.csv")
        except:
            logging.critical(f">>> ERROR: Tires filter parsing ")

        tire_df = pd.read_csv("./utils/all_tires.csv")
        tire_df.drop_duplicates(keep="first", inplace=True)
        for width, height, rimszize, url in tire_df.values:

            yield SeleniumRequest(
                url=url,
                callback=self.parse_tires,
                meta={"width": width, "height": height, "rimsize": rimszize},
            )

    def parse_tires(self, response):
        try:
            url = response.request.url
            name = response.xpath(
                "//div[@class='brand']/following-sibling::h1/text()"
            ).get()
            sku = response.xpath("//span[@class='sku']/text()").get()
            description = "".join(
                response.xpath("//div[@class='pro_size_detail'][1]//text()").getall()
            )
            if description:
                description = description.replace("\n", " ").strip()
            extra_saving_column = "".join(
                response.xpath(
                    "//div[@class='extra_discount clearfix']//text()"
                ).getall()
            ).strip()
            tyre_type = response.xpath("//div[@class='variants']/div/@title").get()
            year_of_manufacture = "".join(
                response.xpath("//div[@title='Year of manufacture']/text()").getall()
            ).strip()

            sidewall = "".join(
                response.xpath(
                    "//li/span[contains(text(),'Sidewall')]/parent::li/text()"
                ).getall()
            ).strip()
            country_of_manufacture = "".join(
                response.xpath("//div[@class='menufacture_country']/text()").getall()
            ).strip()
            manufacturer = response.xpath("//div[@class='brand']/a/@title").get()
            service_desc = response.xpath("//div[@class='serv_desc']/text()[2]").get()
            if service_desc:
                service_desc = service_desc.replace("\n", "").strip()
                tyre_load = service_desc[:-1].strip()
                tyre_speed = service_desc[-1].strip()
            else:
                tyre_load = ""
                tyre_speed = ""

            short_description = name
            if response.xpath("//img[@title='Run Flat']"):
                tyre_run_flat = 1
            else:
                tyre_run_flat = 0

            image_link = response.xpath(
                "//div[@class='product_thumbnail_container']//img[@id='zoom_01']/@src"
            ).get()
            image = extract_filename(image_link)
            thumbnail = image
            small_image = image
            cash_back = response.xpath("//p[@class='prom_text']/text()").get()
            if response.xpath(
                "//p[@class='prom_text']/following-sibling::p[contains(.//text(),'get 1 FREE')]"
            ):
                buy_3_get_1_free = "yes"
            else:
                buy_3_get_1_free = "no"
            type_is_clearance = "".join(
                response.xpath("//div[@class='discount']//text()").getall()
            )
            if type_is_clearance:
                type_is_clearance = type_is_clearance.replace("\n", " ").strip()
            rating_stars = response.xpath(
                "//div[@class='rating-stars']/following-sibling::h3/text()"
            ).get()

            num_reviews = response.xpath("//a[@id='open_review_tab']//text()").get()
            if num_reviews:
                num_reviews = (
                    num_reviews.replace("Reviews", "")
                    .replace("(", "")
                    .replace(")", "")
                    .strip()
                )
            warranty = response.xpath(
                "//div[@class='warranty']/span[@class='w_year']/text()"
            ).get()
            special_price = "".join(
                response.xpath("//span[contains(@id, 'product-price')]/text()").getall()
            ) or "".join(response.xpath("///li[@class='set_price']/text()").getall())
            if special_price:
                special_price.strip()
            price = "".join(
                response.xpath(
                    "//span[contains(@id, 'old-price') or (@class='price')]/text()"
                ).getall()
            )
            if price:
                price = price.strip()
            rim_size = response.meta.get("rimsize")
            if rim_size:
                rim_size = f"R{rim_size}"

            yield {
                "URL": url,
                "sku": sku,
                "name": name,
                "attribute_set": "Default",
                "type": "Simple",
                "categories": get_tyre_category(tyre_type),
                "description": description,
                "short_description": short_description,
                "price": price,
                "qty": 500,
                "is_in_stock": 1,
                "manage_stock": 1,
                "use_config_manage_stock": 1,
                "status": 1,
                "visibility": 4,
                "weight": 1,
                "tax_class_id": "Taxable Goods",
                "image_link": image_link,
                "image": image,
                "thumbnail": thumbnail,
                "small_image": small_image,
                "manufacturer": manufacturer,
                "country_of_manufacture": country_of_manufacture,
                "sidewall": sidewall,
                "special_price": special_price,
                "tyre_width": response.meta.get("width"),
                "tyre_height": response.meta.get("height"),
                "tyre_rim_size": rim_size,
                "tyre_load": tyre_load,
                "tyre_speed": tyre_speed,
                "tyre_type": tyre_type,
                "year_of_manufacture": year_of_manufacture,
                "type_is_clearance": type_is_clearance,
                "buy_3_get_1_Free": buy_3_get_1_free,
                "tyre_run_flat": tyre_run_flat,
                "extra_saving_column": extra_saving_column,
                "cash_back": cash_back,
            }
            download_image(image_link, image)
        except:
            pass
