import datetime
import os
import random
import requests

today = datetime.datetime.utcnow().date().isoformat()

with open("wifi_news_digest_source.txt", "r") as f:
    entries = [line.strip() for line in f if "-->" in line]

sample = random.sample(entries, k=3)
digest = [f"{today}:"]
for entry in sample:
    title, url = entry.split("-->")
    digest.append(f"• {title.strip()}\n  → {url.strip()}")

content = "\n\n".join(digest)

update_url = f"https://api.github.com/gists/{os.environ['GIST_ID']}"
headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
payload = {
    "files": {
        "wifi_news_digest.txt": {
            "content": content
        }
    }
}

response = requests.patch(update_url, json=payload, headers=headers)
if response.status_code != 200:
    raise Exception(f"Failed to update gist: {response.content}")
