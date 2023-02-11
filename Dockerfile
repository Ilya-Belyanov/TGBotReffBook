FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY ./app/ /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]