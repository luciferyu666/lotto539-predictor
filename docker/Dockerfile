FROM python:3.10-slim
WORKDIR /app
COPY src /app/src
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT ["python", "-m", "src.run_pipeline"]
