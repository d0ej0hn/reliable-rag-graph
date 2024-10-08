# The builder image, used to build the virtual environment
FROM python:3.12-bullseye AS builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY reliable_rag_graph ./reliable_rag_graph
COPY .env ./

# Create the google colab folder in venv site-packages to trigger chromadb into using pysqlite3-binary
RUN mkdir /app/.venv/lib/python3.12/site-packages/google/colab

EXPOSE 8000

ENTRYPOINT ["python", "-m", "reliable_rag_graph.server"]