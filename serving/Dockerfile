FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir poetry==1.8.4 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . /app

EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=5s --retries=5 CMD wget -qO- http://localhost:8000/health || exit 1

CMD ["python", "-m", "serving.main"]
