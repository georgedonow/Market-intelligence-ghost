from fastapi import FastAPI
import redis
import json

app = FastAPI()
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/insights")
def get_insights():
    insights = []
    while True:
        data = r.rpop("insights_queue")
        if not data:
            break
        insights.append(json.loads(data))
    return {"insights": insights}
