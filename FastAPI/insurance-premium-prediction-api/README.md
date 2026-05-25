# Insurance Premium Prediction API

A production-ready REST API that predicts insurance premium categories based on user demographics and lifestyle factors. Built with FastAPI, containerized with Docker, and deployed on AWS EC2.

## Tech Stack

- **FastAPI** — REST API framework
- **scikit-learn** — Machine learning model
- **Pydantic v2** — Input validation with computed fields
- **Docker** — Containerization
- **Streamlit** — Frontend interface
- **AWS EC2** — Cloud deployment

## API Endpoints

| Method | Endpoint   | Description                       |
|--------|------------|-----------------------------------|
| GET    | `/`        | API info                          |
| GET    | `/health`  | Health check with model status    |
| POST   | `/predict` | Predict insurance premium category |

### Request Body (`/predict`)

```json
{
  "age": 35,
  "weight": 72.0,
  "height": 1.75,
  "income_lpa": 12.0,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

Fields `bmi`, `age_group`, `lifestyle_risk`, and `city_tier` are derived automatically.

### Response

```json
{
  "predicted_category": "Medium",
  "confidence": 0.8432,
  "class_probabilities": {
    "Low": 0.01,
    "Medium": 0.84,
    "High": 0.15
  }
}
```

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Docker

**Build and run locally:**

```bash
docker build -t kernelcrush/insurance-premium-api .
docker run -p 8000:8000 kernelcrush/insurance-premium-api
```

**Pull from Docker Hub:**

```bash
docker pull kernelcrush/insurance-premium-api:latest
docker run -p 8000:8000 kernelcrush/insurance-premium-api
```

## AWS EC2 Deployment

1. Create and connect to an EC2 instance.

2. Install Docker:

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
exit
```

3. Reconnect to the instance and run the container:

```bash
docker pull kernelcrush/insurance-premium-api:latest
docker run -p 8000:8000 kernelcrush/insurance-premium-api
```

4. Update the EC2 security group to allow inbound traffic on port 8000.

5. Verify the API is running at `http://<EC2-PUBLIC-IP>:8000/health`.

## Streamlit Frontend

```bash
streamlit run frontend.py
```

Update `API_URL` in `frontend.py` to point to your EC2 instance's public IP before running.
