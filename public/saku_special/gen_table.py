import requests
import json
import os

# need to change date in code manually!!!!!!!!!!!!!!!!!!!!!!!!!
# need to change 1,1.5,2,2.5 in last in code!!!!!!!!
# have to use 1.5 instead of 1保 or 1+ because we need to compare 1<1.5<2<2.5<3
last = 2
current = 2.5

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "../headers.json"), "r") as f:
    headers = json.load(f)
fetch_url = f"https://ticket.fortunemeets.app/data/sakurazaka46/2ndAL/config.json"
# https://ticket.fortunemeets.app/data/nogizaka46/35th/config.json

participating_members = [
    "井上梨名",
    "遠藤光莉",
    "大園玲",
    "大沼晶保",
    "幸阪茉里乃",
    "武元唯衣",
    "田村保乃",
    "藤吉夏鈴",
    "増本綺良",
    "松田里奈",
    "森田ひかる",
    "守屋麗奈",
    "山﨑天",
    "石森璃花",
    "遠藤理子",
    "小田倉麗奈",
    "小島凪紗",
    "谷口愛季",
    "中嶋優月",
    "的野美青",
    "向井純葉",
    "村井優",
    "村山美羽",
    "山下瞳月",
]


def fetch_json():
    response = requests.get(fetch_url, headers=headers)
    with open("config.json", "wb") as file:
        file.write(response.content)


def parse_json():
    with open("config.json", "r") as src:
        data = json.load(src)
        result = {}
        for member in participating_members:
            # assume all participate in real meet greet
            result[member] = {
                "5月31日": [],
                "6月1日": [],
            }

            for i in [0, 1, 2, 3, 4]:
                if (
                    member
                    in data["applications"][0]["awards"][2]["applyTable"][i][
                        "closedMembers"
                    ]
                ):
                    result[member]["5月31日"].append(1)
                else:
                    result[member]["5月31日"].append(0)

            for i in [5, 6, 7, 8, 9]:
                if (
                    member
                    in data["applications"][0]["awards"][2]["applyTable"][i][
                        "closedMembers"
                    ]
                ):
                    result[member]["6月1日"].append(1)
                else:
                    result[member]["6月1日"].append(0)

        with open("result_parsed.json", "w") as json_result:
            json.dump(result, json_result, ensure_ascii=False, indent=2)


def gen_json():
    # for i in range(1, 46):
    #     if os.path.exists(f"result_{i}.json"):
    #         last = i
    with open(f"result_{last}.json", "r") as last_json_result:
        with open(f"result_parsed.json", "r") as current_json_result:

            data_current = json.load(current_json_result)
            data = json.load(last_json_result)
            for member in data:
                for date in data[member]:
                    if date != "P":
                        for part in range(5):
                            # print(member, date, part)
                            if (
                                date in data_current[member]
                                and data_current[member][date][part] == True
                                and data[member][date][part] == False
                            ):
                                data[member][date][part] = current
            with open(f"result_{current}.json", "w") as json_result:
                json.dump(data, json_result, ensure_ascii=False, indent=2)


def send_file_to_channel(filename):
    url = f"https://api.telegram.org/{TELEGRAM_BOT_TOKEN}/sendDocument"

    while True:
        try:
            # Open the file in binary mode
            with open(os.path.join(script_dir, filename), "rb") as file:
                # Prepare the request payload
                data = {
                    "chat_id": "-1001982849593",  # Group: "-1002350782955", Channel:"-1001982849593"
                    "caption": datetime.datetime.now().strftime("%Y%m%d-Saku-Special"),
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
    driver.get("http://localhost:5173#ss")
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


import datetime
import time

counter = 0
fetch_json()
parse_json()
gen_json()
while True:
    try:
        current_time = datetime.datetime.now()
        if current_time.second == 0:
            fetch_json()
            parse_json()
            gen_json()
            if not os.path.exists("/mnt/c/windows"):
                get_result_img()
            counter += 1
        print(current_time)
        time.sleep(1)
        if counter == 90:
            break
    except Exception as e:
        print("Error:", e)
        time.sleep(10)
