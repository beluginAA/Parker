FROM python:3.12.2
LABEL project="Parcer Python Image"
COPY ./systemctl.service/python-parcer.service /etc/systemd/system/python-parcer.service
COPY ./systemctl.service/python-parcer.timer /etc/systemd/system/python-parcer.timer
RUN apt update && apt install sudo systemctl -y && \
    pip install loguru pymysql telethon telebot && \
    sudo systemctl daemon-reload && \
    sudo systemctl enable python-parcer.service && \
    sudo systemctl enable python-parcer.timer && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home
