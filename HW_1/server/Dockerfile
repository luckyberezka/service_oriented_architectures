FROM python:3.8

WORKDIR /code

ADD server.py .

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "-u", "server.py"]