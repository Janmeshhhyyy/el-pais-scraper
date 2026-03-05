from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from deep_translator import GoogleTranslator
from collections import Counter
import threading
import time

# BROWSERSTACK CREDENTIALS
USERNAME = "janmeshnaik_Mx1YmS"
ACCESS_KEY = "zzeXpD2Bm6sCk3rmVrkz"

URL = "https://elpais.com/opinion/"

# 5 Browser Configurations
browsers = [
{
"os": "Windows",
"osVersion": "11",
"browserName": "Chrome",
"browserVersion": "latest"
},
{
"os": "Windows",
"osVersion": "11",
"browserName": "Edge",
"browserVersion": "latest"
},
{
"os": "OS X",
"osVersion": "Monterey",
"browserName": "Safari",
"browserVersion": "latest"
},
{
"deviceName": "iPhone 14",
"osVersion": "16",
"realMobile": "true"
},
{
"deviceName": "Samsung Galaxy S22",
"osVersion": "12",
"realMobile": "true"
}
]

translated_titles = []


def run_scraper(cap):
    # Build BrowserStack-specific options using Selenium 4 compatible API
    bstack_options = {
        "userName": USERNAME,
        "accessKey": ACCESS_KEY,
        "buildName": "ElPais Assignment",
        "sessionName": "Opinion Scraper Test",
    }

    # Copy capability entries that describe the environment (OS / browser / device)
    for key in ("os", "osVersion", "browserName", "browserVersion", "deviceName", "realMobile"):
        if key in cap:
            bstack_options[key] = cap[key]

    options = Options()

    # For desktop browsers, set the browserName at the top level as required by W3C
    if "browserName" in cap:
        options.set_capability("browserName", cap["browserName"])

    options.set_capability("bstack:options", bstack_options)

    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub",
        options=options,
    )

    try:

        driver.get(URL)

        time.sleep(5)

        articles = driver.find_elements(By.TAG_NAME, "h2")

        print("\nTop 5 Articles (Spanish):")

        for i, article in enumerate(articles[:5]):

            title = article.text.strip()

            if title != "":

                print(title)

                try:
                    translated = GoogleTranslator(source='auto', target='en').translate(title)
                    translated_titles.append(translated)
                except:
                    translated = title

                print("Translated:", translated)
                print()

    except Exception as e:
        print("Error:", e)

    driver.quit()


threads = []

for browser in browsers:
    thread = threading.Thread(target=run_scraper, args=(browser,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


print("\nAll Translated Titles:")
for t in translated_titles:
    print(t)


# Word Frequency Analysis
words = []

for title in translated_titles:
    words.extend(title.lower().split())

word_count = Counter(words)

print("\nWords repeated more than twice:\n")

for word, count in word_count.items():
    if count > 2:
        print(word, ":", count)