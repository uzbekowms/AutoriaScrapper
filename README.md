# Python Web Scraper for Cars

## Overview
This project aims to build a simple web scraper using Python to extract car information from an autoria and send push notifications to telegram group. The scraper will use BeautifulSoup for parsing HTML and requests for making HTTP requests.

## Dependencies
- Python 3.11
- BeautifulSoup
- requests
- lxml
- APScheduler

I used the APScheduler library to schedule the parser to run every 10 minutes.

## Installation
Install the required dependencies using the following commands:

```bash
pip install pip install -r requirements.txt
```

## With Docker
```bash
docker build -t autoria-scrapper .
docker run -it --rm -name scrapper autoria-scrapper
```
