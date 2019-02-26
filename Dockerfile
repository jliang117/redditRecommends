FROM python:3.6

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r /requirements.txt 
RUN python -m spacy download en


WORKDIR /app
COPY src /app

ENV PORT 8080
CMD ["gunicorn", "app:app", "--config=gconfig.py"]
