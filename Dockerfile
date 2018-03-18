FROM python:3.6

RUN mkdir /app && \
    mkdir /data

ADD . /app

RUN cd /app && \
    pip install -r requirements.txt

EXPOSE 8899

ENTRYPOINT ["python3", "/app/app.py"]
