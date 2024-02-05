FROM python:3.11-alpine3.19

WORKDIR ./app

ADD . .

VOLUME ./cars.db ./cars.db

RUN pip install -r requirements.txt

CMD ["python", "main.py"]