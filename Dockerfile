FROM python:3.12-slim


RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get purge -y curl && apt-get clean


# Set the working directory
WORKDIR /app

# Install poetry
#RUN pipx install poetry==1.8.4

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./
COPY . .
# Install the dependencies
RUN poetry install --no-dev

# Copy the rest of the application code


# Set the entry point to call graphedexcel using poetry
ENTRYPOINT ["poetry", "run", "graphedexcel"]
