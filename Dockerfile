FROM python:3.6.8

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#WORKDIR /app
CMD ["python", "main.py"]
