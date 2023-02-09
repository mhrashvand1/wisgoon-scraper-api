import scrapy
from scraper.items import PostItem
from datetime import datetime


class WisgoonSpider(scrapy.Spider):
    name = "wisgoon"
    
    def __init__(self, name=None, **kwargs):
        self.username = kwargs.get("username")
        # Check that username is sent
        if not self.username:
            raise ValueError("You must enter the username of the page you want to crawl.")
        # Set start urls
        self.start_urls = [
            f"https://wisgoon.com/{self.username}"
        ]
        # Get from_datetime argument
        self.from_datetime = kwargs.get("from_datetime")  
        # Check that from_datetime argument is instance of datetime
        if not isinstance(self.from_datetime, datetime):
            try:
                self.from_datetime = datetime.strptime(
                    self.from_datetime,
                    "%Y-%m-%dT%H:%M:%S"
                )
            except:
                the_origin_of_my_history = "2001-01-20T00:00:00"
                self.from_datetime = datetime.strptime(
                    the_origin_of_my_history,
                    "%Y-%m-%dT%H:%M:%S"
                )        
        super().__init__(name, **kwargs)


    def parse(self, response):
        x_data_attr = response.css("body > section.relative.mx-auto::attr(x-data)").get()
        comma_index = x_data_attr.index(",")
        page_id = x_data_attr[8:comma_index]
        yield scrapy.Request(
            url=f"https://gateway.wisgoon.com/v7/post/user/{page_id}/?before=0",
            callback=self.post_list_parse,
            meta={"before":0, "page_id":page_id}
        )
        
    
    def post_list_parse(self, response):
        res = response.json()
        stop_crawling = False
                
        for obj in res["objects"]:
            create = datetime.strptime(obj["create"], "%Y-%m-%dT%H:%M:%SZ")
            if create > self.from_datetime:
                obj["create"] = create
                item = self.serialize_data(raw_data=obj)
                yield item
            else:
                stop_crawling = True
                break
                   
        if len(res["objects"]) > 0 and not stop_crawling:
            before = response.meta["before"]+10
            page_id = response.meta["page_id"]
            yield scrapy.Request(
                url=f"https://gateway.wisgoon.com/v7/post/user/{page_id}/?before={before}",
                callback=self.post_list_parse,
                meta={"before":before, "page_id":page_id}
            )

     
    def serialize_data(self, raw_data):
        item = PostItem()
        item["username"] = self.username.strip()
        item["source_id"] = raw_data.get("id")
        item["title"] = raw_data.get("title", "").strip()
        item["text"] = raw_data.get("text", "").strip()
        # post create datetime
        created_at = datetime.strftime(raw_data.get("create"), "%Y-%m-%d %H:%M:%S")
        item["source_created"] = created_at
        # Media
        item["media"] = dict()
        # Main Media
        if raw_data.get("video_url"):
            item["media"]["main_media"] = raw_data["video_url"].strip() 
        else:
            item["media"]["main_media"] = raw_data["images"]["original"]["url"].strip()
        # Other Media (slides)
        item["media"]["other_media"] = [item["images"]["original"]["url"].strip() for item in raw_data["slides"]]
        return item