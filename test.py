import time
import os
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
from collections import Counter

# create images folder
if not os.path.exists("images"):
    os.makedirs("images")

driver = webdriver.Chrome()
driver.get("https://elpais.com/opinion/")
time.sleep(5)

# accept cookies
try:
    driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]").click()
    time.sleep(2)
except:
    pass

articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]

titles = []
contents = []

print("\nTop 5 Articles:\n")

for i, article in enumerate(articles):

    try:
        title_element = article.find_element(By.CSS_SELECTOR, "h2 a")
        title = title_element.text
        titles.append(title)

        print(f"{i+1}. {title}")

        link = title_element.get_attribute("href")

        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(3)

        paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
        text = ""

        for p in paragraphs:
            text += p.text + "\n"

        contents.append(text)

        # download image
        try:
            img = driver.find_element(By.CSS_SELECTOR, "figure img")
            img_url = img.get_attribute("src")

            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))

            image = image.convert("RGB")
            image.save(f"images/article_{i+1}.jpg", "JPEG")

            print(f"   Image saved: images/article_{i+1}.jpg")

        except:
            print("   No valid image found")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print("Error:", e)

# translate titles
translated_titles = []

print("\nTranslated Titles:\n")

for title in titles:
    translated = GoogleTranslator(source='es', target='en').translate(title)
    translated_titles.append(translated)
    print(translated)

# save to file
with open("articles.txt", "w", encoding="utf-8") as f:
    for i in range(len(titles)):
        f.write(f"\nARTICLE {i+1}\n")
        f.write(f"Spanish Title: {titles[i]}\n")
        f.write(f"English Title: {translated_titles[i]}\n\n")
        f.write("Content:\n")
        f.write(contents[i])
        f.write("\n\n")

# repeated words
all_words = " ".join(translated_titles).lower().split()
counts = Counter(all_words)

print("\nWords repeated more than twice:\n")

for word, count in counts.items():
    if count > 2:
        print(word, ":", count)

driver.quit()