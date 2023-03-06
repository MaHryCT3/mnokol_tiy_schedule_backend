FROM python:3.11-buster as requirements-stage

WORKDIR /tmp


# Download and setup poetry
RUN pip install poetry

# Create a requirements.txt from poetry files
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LOGURU_LEVEL 'INFO'

WORKDIR /code

# Copy requirements file 
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# Install depencdecies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt install make

COPY ./app/ ./app/
COPY ./Makefile .

EXPOSE 443

CMD ["make", "run-production"]
