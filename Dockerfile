FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src

COPY requirements.txt /usr/src
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
COPY ./app /usr/src/app

ENV PATH="${PATH}:/usr/src/app"

CMD ["python", "main.py"]