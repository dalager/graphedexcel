FROM python:3.11-slim AS builder
RUN pip install --no-cache-dir poetry==1.8.4

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

COPY . .

# Install your package
RUN poetry install --only main --no-interaction --no-ansi

ENV PATH="/app/.venv/bin:$PATH"

RUN ln -s /app/.venv/bin/graphedexcel /usr/local/bin/graphedexcel


# Set the entry point to call graphedexcel using poetry
ENTRYPOINT ["graphedexcel"]
