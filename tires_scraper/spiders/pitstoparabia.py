import scrapy
from tires_scraper.spiders.filter_tires import *
from scrapy_selenium import SeleniumRequest

DEFAULT_VALUES = {
    "attribute_set": "Default",
    "type": "Simple",
    "qty": 500,
    "is_in_stock": 1,
    "manage_stock": 1,
    "use_config_manage_stock": 1,
    "status": 1,
    "visibility": 4,
    "weight": 1,
    "tax_class_id": "Taxable Goods",
}


class PitstoparabiaSpider(scrapy.Spider):
    name = 'pitstoparabia'
    allowed_domains = ['www.pitstoparabia.com']


    def start_requests(self):
        yield SeleniumRequest(url="https://www.pitstoparabia.com/en/advancesearch?dir=asc&form_key=YTop2Giq9qdZ8Ke2&width=221&height=19&rim_size=235&rear_width=&rear_height=&rear_rim_size=&sizelocation=Dubai", callback=self.tires_to_csv)

    def tires_to_csv(self, response):
        driver = response.meta['driver']

        # if you do not wish to extract all tires url again
        # comment the next line of code by adding a '#' character in front
        parse_filters(driver, 'all_tires.csv')
        
        tire_df = pd.read_csv('./utils/all_tires.csv')
        tire_df.drop_duplicates(keep='first', inplace=True)
        for width, height, rimszize, url in tire_df.values:

            yield SeleniumRequest(
                url=url,
                callback=self.parse_tires,
                meta={"width": width, "height": height, "rimsize": rimszize},
            )      
    
    def parse_tires(self, response):
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
            response.xpath("//div[@class='extra_discount clearfix']//text()").getall()
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
        ).strip()
        old_price = "".join(
            response.xpath("//span[contains(@id, 'old-price')]/text()").getall()
        ).strip()
        # TODO: add categories xpath

        yield {
            "URL": url,
            "Manufacturer": manufacturer,
            "Name": name,
            "SKU": sku,
            "Country of Manufacture": country_of_manufacture,
            "Year of Manufacture": year_of_manufacture,
            "Description": description,
            "Short Description": short_description,
            "Width": response.meta.get("width"),
            "Height": response.meta.get("height"),
            "Rim Size": response.meta.get("rimsize"),
            "Service Desc": service_desc,
            "Tyre Load": tyre_load,
            "Tyre Speed": tyre_speed,
            "Tyre Run Flat": tyre_run_flat,
            "Tyre Type": tyre_type,
            "Sidewall": sidewall,
            "Image Link": image_link,
            "Image": image,
            "Thumbnail": thumbnail,
            "Price": special_price,
            "Old Price": old_price,
            "Small Image": small_image,
            "Cash Back": cash_back,
            "Buy 3 get 1 Free": buy_3_get_1_free,
            "Type is Clearance": type_is_clearance,
            "Extra Saving Column": extra_saving_column,
            "Rating Stars": rating_stars,
            "Number of Reviews": num_reviews,
        }




