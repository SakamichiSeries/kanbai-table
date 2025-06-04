import requests
import json
import os
from dotenv import load_dotenv
import base64

entry = 2
fetch_url = f"https://fortunemusic.jp/sakurazaka_202506/{entry+1}/goods_list/"

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
headers = json.loads(base64.b64decode(os.getenv("COOKIE_BASE64")).decode("utf-8"))
# print(headers)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def test_login():
    url = "https://main.fortunemusic.jp/secure/cust/custRev.php?cd=NAME"
    response = requests.get(url, headers=headers)
    lines = response.text.splitlines()
    for i in range(len(lines)):
        if "漢字" in lines[i]:
            for j in range(8):
                print(lines[i + j])
            return True

    print("not logged in")
    print(response.text)
    return False


def fetch_html():

    response = requests.get(fetch_url, headers=headers)

    with open(os.path.join(script_dir, "goods_list.html"), "wb") as file:
        file.write(response.content)


def parse_html():
    with open(os.path.join(script_dir, "goods_list.html"), "r") as file:
        result = ""
        lines = file.read().splitlines()

        include_current = False
        for line in lines:
            if r"toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1]" in line:
                break
            if include_current:
                result += line
            if "var members = (function()" in line:
                include_current = True

        result = json.loads(result)
        with open(os.path.join(script_dir, "result_raw.json"), "w") as json_result:

            json.dump(result, json_result, ensure_ascii=False, indent=2)


def parse_json():
    with open(os.path.join(script_dir, "result_raw.json"), "r") as src:
        data = json.load(src)
        result = {}
        for member in data[0]["members"]:
            result[member["name"]] = {}
            for date in member["venues"]:

                temp = []
                if "parts" in date:
                    for part in date["parts"]:
                        if part["stock"] > 0:
                            temp.append(0)
                        else:
                            temp.append(1)  # lottery index
                    result[member["name"]][date["date"]] = temp

        with open(os.path.join(script_dir, "result_parsed.json"), "w") as json_result:

            json.dump(result, json_result, ensure_ascii=False, indent=2)


def gen_json():
    last = 0
    for i in range(1, 46):
        if os.path.exists(os.path.join(script_dir, f"result_{i}.json")):
            last = i
    with open(os.path.join(script_dir, f"result_{last}.json"), "r") as last_json_result:
        with open(
            os.path.join(script_dir, f"result_parsed.json"), "r"
        ) as current_json_result:

            data_current = json.load(current_json_result)
            data = json.load(last_json_result)
            for member in data:
                for date in data[member]:
                    for part in range(0, 6):
                        # print(member, date, part)
                        if (
                            member in data_current
                            and date in data_current[member]
                            and data_current[member][date][part] > 0
                            and data[member][date][part] == 0
                        ):
                            data[member][date][part] = last + 1
            with open(
                os.path.join(script_dir, f"result_{last+1}.json"), "w"
            ) as json_result:
                json.dump(data, json_result, ensure_ascii=False, indent=2)


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
                    "chat_id": "-1001982849593",  # "chat_id": "-1002350782955",
                    "caption": datetime.datetime.now().strftime("%Y%m%d-Saku"),
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


def get_result_img():
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
    driver.get("http://localhost:5173#s")
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

if test_login():
    while True:
        time.sleep(1)
        tokyo_tz = pytz.timezone("Asia/Tokyo")
        current_hour = datetime.datetime.now(tokyo_tz).hour
        current_min = datetime.datetime.now(tokyo_tz).minute
        current_second = datetime.datetime.now(tokyo_tz).second
        print(current_hour, current_min, current_second, fetch_url)

        if current_hour >= 14 and current_second >= 5:
            try:
                fetch_html()
                parse_html()
                parse_json()
                gen_json()
                send_file_to_channel("goods_list.html")
                if not os.path.exists("/mnt/c/windows"):
                    get_result_img()
                break
            except:
                pass
