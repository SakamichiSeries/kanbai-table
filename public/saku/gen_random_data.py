import os
import json
import random

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

last = 0
for i in range(1, 46):
    if os.path.exists(os.path.join(script_dir, f"result_{i}.json")):
        last = i
with open(os.path.join(script_dir, f"result_{last}.json")) as last_json_result:
    data = json.load(last_json_result)
    for member in data:
        flag_sold_out = True if random.randint(1, 10) > 9 else False
        for date in data[member]:
            for part in range(0, 6):
                # print(member, date, part)
                if data[member][date][part] == 0:
                    if random.randint(1, 10) > 9 or flag_sold_out:
                        data[member][date][part] = last + 1
    with open(os.path.join(script_dir, f"result_{last + 1}.json"), "w") as json_result:
        json.dump(data, json_result, ensure_ascii=False, indent=2)
