import fastapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Correcting the FastAPI initialization
app = fastapi.FastAPI()

@app.get("/")
async def hello():
    return {"hello"}

# Instrumenting the app with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)
