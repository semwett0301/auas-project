FROM python:3.9

WORKDIR /app

COPY ../requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY preparation_module /app/preparation_module

ENV PYTHONPATH=/app

CMD ["python", "/app/preparation_module/index.py"]
