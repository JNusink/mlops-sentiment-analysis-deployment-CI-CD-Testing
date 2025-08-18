# MLOps Sentiment Analysis Deployment CI/CD Testing

Welcome to the MLOps Sentiment Analysis Deployment CI/CD Testing project by JNusink! This repository contains a sentiment analysis application built with FastAPI (API backend) and Streamlit (monitoring dashboard), containerized with Docker, and designed for deployment on AWS EC2 with CI/CD integration. The project uses a pre-trained logistic regression model and TF-IDF vectorizer trained on the IMDB Dataset.csv to predict sentiment (positive/negative) from text input.

## Project Architecture

- **API (FastAPI)**: Handles sentiment prediction requests at `/predict`, logging results to a `sentiment.log` file.
- **Dashboard (Streamlit)**: Displays recent predictions from the log file for monitoring.
- **Docker**: Containers (`sentiment-api` and `sentiment-monitoring`) ensure consistent deployment.
- **AWS EC2**: Target deployment environment with Dockerized containers.
- **CI/CD**: Planned integration with GitHub Actions (to be implemented).

## Local Development Instructions

### Prerequisites
- **Python 3.13.7**: Install from [python.org](https://www.python.org/downloads/) or use the Windows Store version.
- **VS Code**: Install from [code.visualstudio.com](https://code.visualstudio.com/) with Python and Docker extensions.
- **Docker Desktop**: Install from [docker.com](https://www.docker.com/products/docker-desktop/).
- **Git**: Install from [git-scm.com](https://git-scm.com/) to clone the repository.

### Setup
1. Clone the repository:
   ```powershell
   git clone https://github.com/JNusink/mlops-sentiment-analysis-deployment-CI-CD-Testing.git
   cd mlops-sentiment-analysis-deployment-CI-CD-Testing
   ```
2. Create a virtual environment and activate it:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt --only-binary :all:
   ```
4. Verify model and vectorizer files:
   - Ensure `sentiment_model.pkl` and `vectorizer.pkl` are in `api/`.
   - Test with `python api/test_pickle.py`.

### Running Locally
1. Start the FastAPI server:
   ```powershell
   cd api
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```
   - Test at http://localhost:8001/docs with a POST request (e.g., `{"text": "This movie is awesome!"}`).
2. Start the Streamlit dashboard:
   ```powershell
   cd ..\monitoring
   streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   ```
   - View at http://localhost:8501 after a prediction.
3. Stop with Ctrl+C in each terminal.

## Docker Deployment

### Build Images
1. Ensure `Dockerfile` files are in `api/` and `monitoring/`.
2. Build the images from the root directory:
   ```powershell
   docker build -f api/Dockerfile -t sentiment-api .
   docker build -f monitoring/Dockerfile -t sentiment-monitoring .
   ```

### Run Containers
1. Create a shared volume:
   ```powershell
   docker volume create shared-logs
   ```
2. Run the containers:
   ```powershell
   cd api
   docker run -d -p 8000:8000 -v shared-logs:/app/logs --name api-container sentiment-api
   cd ..\monitoring
   docker run -d -p 8501:8501 -v shared-logs:/app/logs --name monitoring-container sentiment-monitoring
   ```
3. Test:
   - API: http://localhost:8001/docs.
   - Dashboard: http://localhost:8501 (after a prediction).
4. Stop and remove containers:
   ```powershell
   docker stop api-container monitoring-container
   docker rm api-container monitoring-container
   ```

### Troubleshooting
- **Port Conflicts**: Use `netstat -aon | findstr :8001` or `:8501`, terminate with `taskkill /PID <PID> /F`.
- **Build Failures**: Ensure `requirements.txt` is accessible (copy to `api/` and `monitoring/` or adjust `Dockerfile`).
- **Container Issues**: Check logs with `docker logs api-container` or `docker logs monitoring-container`.
## Troubleshooting Log Issues
- Ensure `log_dir` in `api/main.py` and `monitoring/app.py` is set to `/app/logs` to match the `shared-logs` volume mount.
- Verify log files are written to the `shared-logs` volume (e.g., `C:\Users\<YourUser>\docker\volumes\shared-logs\_data\sentiment.log`).
## AWS EC2 Deployment

### Launch EC2 Instance
1. Log in to the AWS sandbox console.
2. Navigate to EC2 > Instances > Launch Instance.
3. **Name**: `sentiment-ec2`.
4. **AMI**: `Ubuntu Server 24.04 LTS (HVM), SSD Volume Type`.
5. **Instance Type**: `t2.micro`.
6. **Key Pair**: Create `sentiment-key` (RSA, .pem), download to project directory.
7. **Security Group**: Create `sentiment-sg` with rules:
   - SSH (port 22): Source = "My IP".
   - HTTP (port 8000): Source = "Anywhere-IPv4" (0.0.0.0/0).
   - Custom TCP (port 8501): Source = "Anywhere-IPv4" (0.0.0.0/0).
8. **Storage**: Default (8 GiB gp3).
9. Launch and note the public IP (e.g., `3.14.15.92`).

### SSH and Setup
1. SSH into the instance:
   ```bash
   ssh -i "C:/VS code/mlops-sentiment-analysis-deployment-CI-CD-Testing/sentiment-key.pem" ubuntu@YOUR_EC2_IP
   ```
2. Update and install dependencies:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install git docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   exit
   ssh -i "C:/VS code/mlops-sentiment-analysis-deployment-CI-CD-Testing/sentiment-key.pem" ubuntu@YOUR_EC2_IP
   ```

### Deploy Containers
1. Clone and build:
   ```bash
   git clone https://github.com/JNusink/mlops-sentiment-analysis-deployment-CI-CD-Testing.git
   cd mlops-sentiment-analysis-deployment-CI-CD-Testing
   git checkout dev
   docker volume create shared-logs
   cd api
   docker build -t sentiment-api .
   docker run -d -p 8000:8000 -v shared-logs:/app/logs --name api sentiment-api
   cd ../monitoring
   docker build -t sentiment-monitoring .
   docker run -d -p 8501:8501 -v shared-logs:/app/logs --name monitoring sentiment-monitoring
   ```
2. Test:
   - API: http://YOUR_EC2_IP:8000/docs.
   - Dashboard: http://YOUR_EC2_IP:8501.

## CI/CD Pipeline
- **Planned**: Integrate with GitHub Actions for automated testing and deployment.
- **Setup**: Create `.github/workflows/ci.yml` with test and build steps (to be implemented).

## Troubleshooting
- **Local Issues**: Check port availability, ensure files are in place.
- **Docker Issues**: Verify image builds, check container logs.
- **EC2 Issues**: Confirm security group rules, `.pem` file permissions.

## Project Structure
```
C:\VS code\mlops-sentiment-analysis-deployment-CI-CD-Testing\
├── api\
│   ├── Dockerfile
│   ├── main.py
│   ├── test_api.py
│   ├── train_vectorizer.py
│   ├── sentiment_model.pkl
│   ├── IMDB Dataset.csv
│   ├── vectorizer.pkl
│   ├── test_pickle.py
│   ├── logs\
│       ├── sentiment.log
├── monitoring\
│   ├── Dockerfile
│   ├── app.py
│   ├── test_dashboard.py
├── .github\
│   └── workflows\
├── .venv\
├── requirements.txt
├── .gitignore
├── README.md
```