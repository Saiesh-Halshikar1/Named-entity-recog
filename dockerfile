# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Download the specific spaCy model needed for the application
RUN python -m spacy download en_core_web_sm

COPY . .

# Expose the port that the app runs on
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
