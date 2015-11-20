# Webreg Scrapy

> This is a web scraper for retrieving UCI course information from the [UCI University Registrar](https://www.reg.uci.edu/perl/WebSoc). This is a tool I built for the [UCI Course API](https://github.com/djchie/uci-course-api).

## Table of Contents

1. [Usage](#usage)
    1. [Process](#process)
1. [Requirements](#requirements)
1. [Development](#development)
    1. [Installing Dependencies](#installing-dependencies)
    1. [Running the Scraper](#running-the-scraper)
    1. [Handling UCI Data Changes](#handling-uci-data-changes)
    1. [Roadmap](#roadmap)
1. [Contributing](#contributing)

## Usage

> Use this scraper to grab course information and import it into a PostgreSQL database

### Process

1. Scraper is hosted on Heroku
1. Executes the department spider to grab updated list of departments
1. Executes a course spider for each department in department list
1. Uploads all the information to the AWS RDS PostgreSQL database

## Requirements

- PostgreSQL

## Development

### Installing Dependencies

From within the root directory:

```sh
pip install -r requirements.txt
```

### Running the Scraper

Start up PostgreSQL server with correct relations setup

```sh
// To crawl courses into database
scrapy crawl course_scrapy  
// To crawl courses into database and store them into courses.json
scrapy crawl course_scrapy -o courses.json
```

### Handling UCI Data Changes

1. Change items.py
1. Change the way course_spider.py parses
1. Change the models.py to reflect database schema
1. Change pipelines.py to manage the insertion of new data

### Roadmap

View the project roadmap [here](https://github.com/djchie/uci-course-api/issues)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.