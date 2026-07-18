from fastapi import FastAPI

app = FastAPI(title="Food Tracker API")


@app.get("/health")
def health_check():
    return {"status": "ok"}