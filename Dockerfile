FROM python:alpine3.10
ENV PYTHONBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]
