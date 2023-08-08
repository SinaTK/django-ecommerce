FROM python:latest

LABEL name="Django-Eccomerce"
LABEL version="1.0"

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD [ "gunicorn", "ecommerce.wdgi", "8000" ]
