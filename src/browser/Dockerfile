FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["python", "-m", "browser"]
