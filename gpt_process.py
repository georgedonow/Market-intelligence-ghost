import os, json, redis, time
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_next_data():
    data = r.brpop("processed_data_queue", timeout=5)
    if data:
        return json.loads(data[1])
    return None

def analyze_data(text):
    prompt = f"Extract key market intelligence insights from the following text:\n\n{text}\n\nProvide bullet points."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert market analyst."},
                  {"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        item = get_next_data()
        if item:
            raw_text = item.get('data', '')
            insights = analyze_data(raw_text)
            print("Generated insights:", insights)
            r.lpush("insights_queue", json.dumps({
                "timestamp": item["timestamp"],
                "insights": insights
            }))
        else:
            time.sleep(10)
