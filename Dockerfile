FROM python:3.9.19-slim-bullseye

RUN apt-get update && \ 
    apt-get upgrade && \
    python3 -m pip install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV TABLE_ID='dataset.table_name'
ENV PORT=8000

EXPOSE ${PORT}

CMD uvicorn main:app --host=0.0.0.0 --port="$PORT"