FROM python:3.10-slim-buster

RUN mkdir /opt/bot

RUN pip install --upgrade pip

COPY requirements.txt /opt/bot
RUN pip install -r /opt/bot/requirements.txt

COPY config.cfg /opt/bot/
COPY dto /opt/bot/dto
COPY *.py /opt/bot/
COPY service /opt/bot/service
COPY handlers /opt/bot/handlers

RUN ls /opt/bot

WORKDIR /opt/bot
ENTRYPOINT ["python3","/opt/bot/jenkins-bot.py"]
