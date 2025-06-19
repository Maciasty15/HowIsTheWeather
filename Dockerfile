FROM python:3.11-slim

RUN mkdir /app
COPY pyproject.toml /app
COPY uv.lock /app
WORKDIR /app

RUN pip install uv

RUN uv sync

COPY . /app


ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8050

CMD ["python", "run.py"]
