FROM python:3.13-slim@sha256:751d8bece269ba9e672b3f2226050e7e6fb3f3da3408b5dcb5d415a054fcb061 AS builder

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx

ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry
WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

COPY . .

# Install your package
RUN poetry install --only main --no-interaction --no-ansi

# Runtime stage
FROM python:3.13-slim@sha256:751d8bece269ba9e672b3f2226050e7e6fb3f3da3408b5dcb5d415a054fcb061

LABEL org.opencontainers.image.source=https://github.com/dalager/graphedexcel
LABEL org.opencontainers.image.description="Graphedexcel will take an Excel file and create a graph datastructure and a visualisation of the graph."
LABEL org.opencontainers.image.licenses=MIT


WORKDIR /app

# Install minimal runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends libopenblas-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy only what's needed
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH"

# Create symlink for the executable
RUN ln -s /app/.venv/bin/graphedexcel /usr/local/bin/graphedexcel

ENTRYPOINT ["graphedexcel"]