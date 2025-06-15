import requests
import json
import os
from dotenv import load_dotenv
import base64
import subprocess


# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
headers = json.loads(base64.b64decode(os.getenv("COOKIE_BASE64")).decode("utf-8"))
# print(headers)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


import datetime
import time

import os


def send_file_to_channel(filename):
    url = f"https://api.telegram.org/{TELEGRAM_BOT_TOKEN}/sendDocument"

    while True:
        try:
            # Open the file in binary mode
            with open(os.path.join(script_dir, filename), "rb") as file:
                # Prepare the request payload
                data = {
                    "chat_id": "-1001982849593",  # Group: "-1002350782955", Channel:"-1001982849593"
                    "caption": datetime.datetime.now().strftime("%Y%m%d-Test"),
                }
                files = {"document": file}

                # Send the POST request to Telegram API
                response = requests.post(url, data=data, files=files)

                # Check if the request was successful
                if response.status_code == 200:
                    print("File sent successfully!")
                    break
                else:
                    print(f"Failed to send file: {response.status_code}")
                    print("Response:", response.json())
                    time.sleep(100)

        except Exception as e:
            print("Error:", e)
            time.sleep(100)


def get_result_img(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from PIL import Image
    from io import BytesIO

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--user-data-dir=/tmp/chrome-user-data-{os.getpid()}")
    chrome_options.add_argument("--window-size=1920,3840")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(5)
    element = driver.find_element(By.XPATH, "//img")
    src = element.get_attribute("src")
    import base64

    with open("result.png", "wb") as f:
        f.write(base64.b64decode(src.replace("data:image/png;base64,", "")))

    # element.screenshot("result.png")  # saves new cropped image
    # print("Image saved as result.png")
    os.rename("result.png", os.path.join(script_dir, "result.png"))
    send_file_to_channel("result.png")

    # # https://stackoverflow.com/questions/74398324/python-how-to-take-screenshot-of-div
    # location = element.location
    # size = element.size
    # png = driver.get_screenshot_as_png()
    # print(f"Image Size: {size}")

    # im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

    # left = location["x"]
    # top = location["y"]
    # right = location["x"] + size["width"]
    # bottom = location["y"] + size["height"]
    # im.save("page.png")
    # os.rename("page.png", os.path.join(script_dir, "page.png"))
    # send_file_to_channel("page.png")

    # im = im.crop((left, top, right, bottom))  # defines crop points
    # im.save("result.png")  # saves new cropped image
    # print("Image saved as result.png")
    # os.rename("result.png", os.path.join(script_dir, "result.png"))
    # send_file_to_channel("result.png")
    driver.quit()


import pytz

try:
    get_result_img("http://localhost:5173#n")
    # get_result_img("http://localhost:5173#s")
    #get_result_img("http://localhost:5173#sa")
    get_result_img("http://localhost:5173#h")
    #get_result_img("http://localhost:5173#ns")
    
except:
    pass
