FROM python:3.10-slim

WORKDIR /app

# Copy predictor source (assumed to be cloned next to this template)
COPY . /app/template
# 👇 adapt as needed: bring in main repo one level up
# COPY ../lotto539-predictor /app/lotto539-predictor

RUN pip install --no-cache-dir -r /app/lotto539-predictor/requirements.txt

ENV PYTHONPATH=/app/lotto539-predictor

CMD ["bash", "/app/template/run_prediction.sh"]