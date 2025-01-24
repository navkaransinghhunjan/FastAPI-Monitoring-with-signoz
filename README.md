# SigNoz Monitoring with FastAPI

This repository provides step-by-step instructions to integrate SigNoz with a FastAPI application for monitoring and observability.

## Prerequisites

1. Docker and Docker Compose installed on your system.

2. Python 3.7+ installed along with pip.

3. A basic understanding of FastAPI and OpenTelemetry.

4. Ensure the following Python packages are available:

* fastapi

* uvicorn

* opentelemetry-api

* opentelemetry-sdk

* opentelemetry-instrumentation

* opentelemetry-exporter-otlp

## Getting Started

### Step 1: Setting Up SigNoz

1. Clone the SigNoz repository:
```
git clone https://github.com/SigNoz/signoz.git
cd signoz/deploy/
```
2. Start the SigNoz stack using Docker Compose:
```
docker compose -f docker/clickhouse-setup/docker-compose.yaml up -d
```
3. Verify SigNoz services are running:
```
docker ps
```
SigNoz UI will be available at http://localhost:3301.

### Step 2: Creating the FastAPI Application

1. Create a new FastAPI application:

```app.py```:
```
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, SigNoz!"}

# Instrument the FastAPI application
FastAPIInstrumentor.instrument_app(app)
```

2. Install the necessary Python packages:
```
pip install fastapi uvicorn opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation opentelemetry-exporter-otlp
```

3. Run the FastAPI application with OpenTelemetry instrumentation:
```
OTEL_RESOURCE_ATTRIBUTES="service.name=fastapiApp" \
OTEL_EXPORTER_OTLP_ENDPOINT="http://<COLLECTOR_IP>:4317" \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
opentelemetry-instrument uvicorn app:app --host 0.0.0.0 --port 8000
```
Replace ```<COLLECTOR_IP>``` with the IP address of the SigNoz OpenTelemetry collector. You can find it using:
```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' signoz-otel-collector
```
### Step 3: Verify Monitoring

1. Make a request to the FastAPI application:
```
curl http://localhost:8000/
```
2. Open SigNoz UI at http://localhost:3301 and navigate to the Traces section to see the telemetry data from your FastAPI app.

## Troubleshooting

* Error: ModuleNotFoundError: No module named 'opentelemetry'
Ensure you are running the application in a virtual environment with all required packages installed.

* Error: StatusCode.UNAVAILABLE
Verify the OpenTelemetry Collector endpoint and ensure it is reachable from your FastAPI container or host machine.

