FROM python:alpine

#dependancies for numpy (needed for pandas)
RUN apk update
RUN apk add \
    build-base \
    freetds-dev \
    g++ \
    gcc \
    tar \
    gfortran \
    gnupg \
    libffi-dev \
    libpng-dev \
    libsasl \
    openblas-dev \
    openssl-dev 

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV FLASK_APP=project

# Bundle app source
COPY . .

EXPOSE 80
CMD [ "flask", "run", "--host","0.0.0.0","--port","5000"]
