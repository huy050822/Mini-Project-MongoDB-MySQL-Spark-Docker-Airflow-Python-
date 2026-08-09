# FROM python:3.10
# WORKDIR /main
# COPY . .
# RUN pip install --no-cache-dir -r requirements.txt
# CMD ["python","main.py"]



FROM apache/airflow:2.8.1-python3.10

USER root
# 1. Cài đặt OpenJDK (Bắt buộc phải có Java để PySpark chạy)
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean

USER airflow

# 2. Copy file requirements và cài đặt các thư viện Python
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt