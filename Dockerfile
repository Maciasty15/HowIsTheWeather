FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN python -m venv .venv \
 && .venv/bin/pip install --upgrade pip \
 && .venv/bin/pip install uv \
 && .venv/bin/uv sync

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8050

CMD ["python", "run.py"]
