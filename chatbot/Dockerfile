FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code/src:/code/tests

RUN apt update -y && \
    apt install curl -y && \
    pip install --upgrade pip && \
    pip install poetry setuptools && \
    poetry config virtualenvs.create false

WORKDIR /code

COPY pyproject.toml poetry.lock* README.md ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["uvicorn", "chatbot.web.application:app", "--host", "0.0.0.0", "--port", "8000"]
