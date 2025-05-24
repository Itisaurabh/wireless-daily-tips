import datetime
import os
import requests

# Get today's date in yyyy-mm-dd format
today = datetime.datetime.utcnow().date().isoformat()

# Read tips file
with open("wireless_tips_1_year.txt", "r") as file:
    tips = file.readlines()

# Find today's tip
today_tip = next((line for line in tips if line.startswith(today)), None)

if not today_tip:
    raise Exception("No tip found for today!")

# Prepare the payload
update_url = f"https://api.github.com/gists/{os.environ['GIST_ID']}"
headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
payload = {
    "files": {
        "gistfile1.txt": {
            "content": today_tip.strip()
        }
    }
}

response = requests.patch(update_url, json=payload, headers=headers)
if response.status_code != 200:
    raise Exception(f"Failed to update gist: {response.content}")
