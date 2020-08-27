FROM python:3.8

RUN pip install poetry

COPY . /discord-playing

WORKDIR /discord-playing

RUN poetry config virtualenvs.create false \
    && poetry install