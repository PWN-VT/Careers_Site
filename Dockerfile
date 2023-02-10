FROM python:latest

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV FLASK_APP=project

# Bundle app source
COPY . .

#create uploads folder
RUN mkdir project/uploads

EXPOSE 80
CMD [ "flask", "run", "--host","0.0.0.0","--port","5000"]
