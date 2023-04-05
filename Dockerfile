# Dockerfile, Image, Container
FROM python:3.8

# Install ODBC driver and its dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for ODBC configuration
ENV ODBCINI=/etc/odbc.ini
ENV ODBCSYSINI=/etc

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "./run.py" ]