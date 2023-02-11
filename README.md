# Wisgoon Scraper API 

## Navigation 
- [Description](#description)
  - [What is the Wisgoon Scraper API?](#what-is-the-wisgoon-scraper-api)
  - [Notes](#notes)
- [Run](#run)
- [URLs](#urls)  
  - [Main URL](#main-url)
  - [Post List](#post-list)
  - [Post Detail](#post-detail)
  - [Admin Panel](#admin-panel)

-----
## Description  

### What is The Wisgoon Scraper API?  
The Wisgoon scraper API, composed of Django Rest Framework, Scrapy, and Celery, takes a Wisgoon page username and runs a task through Celery in the background to collect data from that page using Scrapy. It immediately returns a response containing a URL where you can view the scraped data list of the page, including all its posts.    

### Notes

- The page you want to crawl must be public, otherwise no posts will be scraped. 

- If the worker is currently working on a task that scrapes the page with username "x", and you make a request to scrape the data of the page with username "x" again, a new task will not be run.  

- If you have previously scraped the posts from page "x" and now you do it again, only the new posts will be scraped and added to the database.   

- The data collected for each post includes the source ID, title, text, source creation date, and all media associated with that post.
Please note that "source" refers to the ID and creation time of the post on Wisgoon. 

- The display order of posts for each page is based on source_created, which you can change or filter based on. You can also search the title and text of posts.  

- By running the project, a superuser will be generated with username "rashvand" and password "1234", which you can use to log in to the admin panel.



-----  
## Run  

Clone and navigate to the `wisgoon-scraper-api` directory:

``` shell  
git clone git@github.com:mhrashvand1/wisgoon-scraper-api.git  
cd wisgoon-scraper-api 
```  

Then run:

``` shell   
docker-compose -f docker-compose.dev.yml up --build  
```  

Wait until the program is ready to use. You can tell the program is ready when you see logs similar to the following in the terminal: 
``` shell   
wisgoon-scraper-api | [2023-02-11 12:08:42 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
wisgoon-scraper-api | [2023-02-11 12:08:42 +0000] [1] [INFO] Using worker: sync
wisgoon-scraper-api | [2023-02-11 12:08:42 +0000] [19] [INFO] Booting worker with pid: 19

```

-----
## URLs  

### Main URL  
POST: `127.0.0.1`   
Payload:   

``` json 
{
    "username":"<page_username>"
}
```  
If the request is successful, the response will be something like:      
``` json 
{
    "detail": "The page is being        crawled in the background and        theresults can be viewed at the        URL below.",
    "url": "http://127.0.0.1:80/<page_username>/posts/"
}
```  
### Post List
GET: `127.0.0.1/<page_username>/posts`    
If the request is successful, the response will be something like:   
  
``` json   
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "source_id": 37297823,
            "title": "",
            "text": "🔵\nاخرین بازی با حضور تماشاگر قبل کرونا مقابل نفت مسجد سلیمان",
            "main_media": "https://irs01.wisgoon.com/irs01/3d/4b/91/60/irs01_s3old_633x364_DhFyDORQ_1958450_1644785317699660503.jpeg",
            "other_media": [],
            "source_created": "2022-02-13T20:48:37Z",
            "url": "https://wisgoon.com/pin/37297823/",
            "detail": "http://127.0.0.1:80/mohammadhoseinrashvand/posts/37297823/"
        },
        {
            "id": 6,
            "source_id": 37297179,
            "title": "",
            "text": "❤💙",
            "main_media": "https://irs01.wisgoon.com/irs01/9d/cf/ba/c6/irs01_s3old_1023x1280_CPnH5kD6_1958450_1644782124619008345.jpeg",
            "other_media": [],
            "source_created": "2022-02-13T19:55:24Z",
            "url": "https://wisgoon.com/pin/37297179/",
            "detail": "http://127.0.0.1:80/mohammadhoseinrashvand/posts/37297179/"
        }
    ]
}
```     
### Post Detail
GET: `127.0.0.1/<page_username>/posts/<source_id>/` 

If the request is successful, the response will be something like:   

``` json   
{
    "id": 6,
    "source_id": 37297179,
    "title": "",
    "text": "❤💙",
    "main_media": "https://irs01.wisgoon.com/irs01/9d/cf/ba/c6/irs01_s3old_1023x1280_CPnH5kD6_1958450_1644782124619008345.jpeg",
    "other_media": [],
    "source_created": "2022-02-13T19:55:24Z",
    "url": "https://wisgoon.com/pin/37297179/",
    "detail": "http://127.0.0.1:80/mohammadhoseinrashvand/posts/37297179/"
}
```
### Admin Panel      
`127.0.0.1/admin/`  

-----