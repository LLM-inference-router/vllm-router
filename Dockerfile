FROM python:3.10-slim

RUN apt-get update && apt-get install -y wget curl
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
COPY *.py /app
EXPOSE 8000

RUN pip install -r requirements.txt
# CMD ["uvicorn", "main:app", "--host", "8000", "--reload"]
