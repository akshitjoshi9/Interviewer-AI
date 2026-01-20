from fastapi import FastAPI

app = FastAPI(title="FastAPI Starter")

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}
