# Commands to run:

  - scrapy crawl course_scrapy -o courses.json
    - To crawl courses and store them into courses.json

# TODO:

  - Uci api
    - Define database
    - Pipeline information into database
    - Figure out efficient cron job setup
      - put everything into one file?
    - Create a node-express-postgres api
    - Create a endpoints
      - course number
      - course name string
      - in documentation, say can define more endpoints upon request
    - Deploy api and database somehow...
    - Format data that enters into database
  
## Process:

  - Execute the department spider to grab updated list of departments
  - Execute a course spider for each department in department list
  - Upload all the information to Parse
    - https://realpython.com/blog/python/web-scraping-with-scrapy-and-mongodb/

## When UCI Changes Data
  
  - Change items.py
  - Change the way course_spider.py parses
  - Change the models.py to reflect database schema
  - Change pipelines.py to manage the insertion of new data