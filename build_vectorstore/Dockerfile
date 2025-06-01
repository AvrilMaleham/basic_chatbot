FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["sh", "-c", "python build.py && touch /app/vectorstore/.ready"]

