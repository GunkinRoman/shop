FROM python:3.11
 
WORKDIR /src

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./src ./
