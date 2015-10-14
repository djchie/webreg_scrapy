# Commands to run:
- To crawl courses into database
  - scrapy crawl course_scrapy  
- To crawl courses into database and store them into courses.json
  - scrapy crawl course_scrapy -o courses.json

# TODO:
- Set up logging
- Implement APScheduler for periodic jobs on Heroku
  
## Process:
- Scraper is hosted on Heroku
- Executes the department spider to grab updated list of departments
- Executes a course spider for each department in department list
- Uploads all the information to the AWS RDS PostgreSQL database

## When UCI Changes Data:
- Change items.py
- Change the way course_spider.py parses
- Change the models.py to reflect database schema
- Change pipelines.py to manage the insertion of new data