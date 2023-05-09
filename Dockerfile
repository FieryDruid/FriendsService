FROM python:3.10.10-slim-bullseye

WORKDIR /opt/FriendsService

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

RUN pip install poetry==1.4.2 --no-cache-dir && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /opt/FriendsService/
RUN poetry install --without dev --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache/ && \
    rm -rf ~/.cache/pypoetry/artifacts/

COPY . /opt/FriendsService/

RUN chmod +x run.sh

EXPOSE 8000

CMD ./run.sh