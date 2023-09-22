FROM python:3.9-alpine
WORKDIR /app
RUN pip install kubernetes
COPY index.py /app/index.py
CMD ["python", "/app/index.py"]
