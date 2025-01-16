FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]