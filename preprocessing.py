import redis
import json

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def clean_text(data):
    return data.replace("\n", " ").strip()

if __name__ == "__main__":
    while True:
        raw = r.brpop("raw_data_queue", timeout=5)
        if raw:
            data = eval(raw[1])
            cleaned = clean_text(str(data.get("data", "")))
            r.lpush("processed_data_queue", json.dumps({
                "timestamp": data["timestamp"],
                "data": cleaned
            }))
