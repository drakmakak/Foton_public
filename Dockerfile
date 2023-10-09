FROM python:3.11-slim
LABEL authors="kalab"

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY req.txt .

RUN pip install -r req.txt

COPY . .

RUN chmod a+x docker/app.sh

#RUN alembic upgrade head
#
#WORKDIR src
#
CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000