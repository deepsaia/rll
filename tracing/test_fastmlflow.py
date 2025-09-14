import os
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import mlflow

# Set tracking URI (optional but recommended)
os.environ["MLFLOW_TRACKING_URI"] = "./mlruns"

# Initialize FastAPI app
app = FastAPI(title="My FastAPI + MLflow App")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!", "mlflow_endpoint": "/mlflow"}

# NEW WAY: Import MLflow's built-in Flask app directly
from mlflow.server import app as mlflow_app

# Mount MLflow UI under /mlflow
app.mount("/mlflow", WSGIMiddleware(mlflow_app))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_fastmlflow:app", host="127.0.0.1", port=8000, reload=True)