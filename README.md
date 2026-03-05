# EL PAÍS Opinion Section Web Scraper

This project uses Selenium and Python to scrape articles from the EL PAÍS Opinion section.

## Features

- Opens https://elpais.com using Selenium
- Navigates to the Opinion section
- Extracts the first 5 articles
- Saves article titles and content
- Downloads article cover images
- Translates Spanish titles into English
- Performs word frequency analysis on translated titles

## Output Files

articles.txt – Contains:
- Spanish title
- English translation
- Article content

images/ – Contains:
- Article cover images

## Technologies Used

- Python
- Selenium
- BeautifulSoup
- deep-translator
- Pillow

## How to Run

Install dependencies:

pip install selenium deep-translator beautifulsoup4 pillow

Run the script:

python test.py

## Cross Browser Testing

The scraper was executed on BrowserStack across:

- Windows 11 – Chrome
- Windows 11 – Edge
- MacOS – Safari
- iPhone 14
- Samsung Galaxy S22

All tests were executed in parallel threads.