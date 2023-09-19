FROM python:3.10

RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
