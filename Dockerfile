FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
