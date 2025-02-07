FROM python:3.12-slim

ENV SRC_DIR=/opt

ENV APP_DIR=$SRC_DIR/app

WORKDIR $APP_DIR

ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PATH="/$SRC_DIR/.local/bin:${PATH}"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ $APP_DIR

EXPOSE 8000
