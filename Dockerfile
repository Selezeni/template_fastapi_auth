FROM python:3.11

WORKDIR /app

ENV PYTHODONTWRITEBYTECODE = 1
ENV PYTHONNUNBUFFERED = 1

COPY requirements.txt .

RUN apt update
RUN apt-get install -y python3-dev musl-dev libpq-dev gcc cargo

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app