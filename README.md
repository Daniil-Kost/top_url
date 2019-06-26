#### Welcome to "**Top Url**" (http://url2.top) repository!

**This service define:** 
1) Simple UI interface for creating short url link and get stats for it
2) REST API interface for cooperation through json data and get short urls with stats for them


_******_API Swagger docs:_******_ https://app.swaggerhub.com/apis/lemk1/top_url_api/1.0.0#/

##### **How to use main endpoints of '_Top Url_' REST API?:**

1). Register through POST Registration endpoint:
  - You need to define json dict with "username", "password", and "confirm_password" fields
 
      Example: `{"username": "demo", "password": "Test2019", "confirm_password": "Test2019"}`
      
 - POST this data to this address: http://url2.top/api/v1/register
 - get from response Authorization Token like this: `85d70ea13a05f6611ea0ccd69674dd81337accd3b6f186da95df9e120fa32ac...`
 - define this Token in Authorization request header: `{"Authorization": f"Token 844895y45yrrtgrgrgree"}`
 
   After that you will be auth and you can use all API endpoints
  
2). Create short url through POST url endpoint (required Auth Token in headers): 
  - You need to define dict with url field
    
    Example: `{"url": "https://docs.djangoproject.com/en/2.1/ref/models/querysets/"}` 
   
   - POST this data to this address: http://url2.top/api/v1/urls
   - get result from response with short url and stats for it
   
   Example: `{
        "uuid": "e138e75b-a5bd-4568-a841-f8a3f018e853",
        "url": "https://docs.djangoproject.com/en/2.1/ref/models/querysets/",
        "title": "Query Sets",
        "short_url": "http://url2.top/jWcTOg22",
        "clicks": 0,
        "create_dttm": "2019-06-15 11:55:32.578040+03:00"
    }`

3). Get all your created urls (required Auth Token in headers):
   - Send GET request to this address: http://url2.top/api/v1/urls
   - Get all your created urls and stats for them
   
   Example: `[
    {
        "uuid": "e138e75b-a5bd-4568-a841-f8a3f018e853",
        "url": "https://stackoverflow.com/questions/2444899/insert-or-update-on-table-violates-foreign-key-constraint",
        "title": "insert or update on table violates foreign key constraint",
        "short_url": "http://localhost:8000/jEcPEg22",
        "clicks": 0,
        "create_dttm": "2019-05-15 11:55:32.578040+03:00"
    },
    {
        "uuid": "2e2ca33a-d9b8-496b-b47a-c092d8d7082b",
        "url": "https://marshmallow.readthedocs.io/en/3.0/",
        "title": "marshmallow: simplified object serialization¶",
        "short_url": "http://localhost:8000/rvkoVaoq",
        "clicks": 4,
        "create_dttm": "2019-05-15 16:03:33.428849+03:00"
    }
]`

##### Also you can use all another endpoints (please read Swagger docs about usage them)