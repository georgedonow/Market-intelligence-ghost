import time, requests
import redis
from datetime import datetime

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def fetch_source_data():
    url = "https://www.reddit.com/r/marketnews/new.json"
    headers = {"User-Agent": "MarketIntelligenceGhostBot/1.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == "__main__":
    while True:
        data = fetch_source_data()
        if data:
            message = {
                "timestamp": datetime.utcnow().isoformat(),
                "source": "reddit",
                "data": data
            }
            r.lpush("raw_data_queue", str(message))
            print("Data enqueued at", message["timestamp"])
        time.sleep(300)
