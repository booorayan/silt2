FROM python:3.10

#set unbuffered output for python
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y && apt install -y build-essential

#specify app dir
WORKDIR /app

#install app dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

#copy app dir files
COPY . .

#expose server port
EXPOSE 8000

#make script executable
RUN chmod +x django.sh

#entrypoint to run the django.sh file
ENTRYPOINT ["/app/django.sh"]