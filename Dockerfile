#https://airflow.apache.org/docs/docker-stack/build.html#adding-packages-from-requirements-txt

FROM apache/airflow:2.7.0-python3.11

USER root

RUN apt-get update \
    && ACCEPT_EULA=Y apt-get upgrade -y \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y libpq-dev gcc \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

USER airflow

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
