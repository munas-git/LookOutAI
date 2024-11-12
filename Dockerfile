FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /LookOutAI
COPY . /LookOutAI

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run the main application
CMD ["python", "app/app.py"]