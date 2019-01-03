FROM python:3.6

ADD /app /app

ADD /docker /docker

RUN pip install -r /docker/requirements.txt

WORKDIR /app

CMD ["python", "-u", "/app/mn_dnr_lookup.py"]