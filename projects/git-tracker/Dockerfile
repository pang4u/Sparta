FROM python:3.8-slim
ADD . /app
WORKDIR /app
RUN pip install flask pymongo bs4 requests parse markdown
CMD ["python", "app.py"]