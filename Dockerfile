FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3-tk \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

CMD ["python", "module1_search_location.py"]