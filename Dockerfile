FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir requests redis openai fastapi uvicorn
CMD ["python", "preprocessing.py"]
