# Python Web Scraper for Cars

## Overview
This project aims to build a simple web scraper using Python to extract car information from an autoria and send push notifications to telegram group. The scraper will use BeautifulSoup for parsing HTML and requests for making HTTP requests.


[Telegram group](https://t.me/+GOtqkkBEyMI1MzQy)

## Problems
In this project, the main challenge was Telegram's limitation on the number of messages sent by the bot, so it was necessary to introduce delays between sending messages.

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
