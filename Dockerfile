FROM python:3.5.2
MAINTAINER furion <_@furion.me>

COPY . /src
WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
