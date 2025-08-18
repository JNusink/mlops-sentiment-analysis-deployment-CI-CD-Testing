FROM python:3.13-slim
WORKDIR /app
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY monitoring/. .
ENV DOCKER_ENV=1
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]