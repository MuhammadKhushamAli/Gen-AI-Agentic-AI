from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import processor

app = FastAPI()

@app.get("/")
def home():
    return { "status": "Server is up and running" }

@app.post("/chat")
def chat(
    query: str = Query(..., description="The user input")
):
    job = queue.enqueue(processor, query)

    return { "status": "OK", "job_id":job.id }

@app.get("/response")
def response(
    job_id: str = Query(..., description="The ID of job which is queued")
):
    job = queue.fetch_job(job_id)
    result = job.return_value()
    return { "status": "OK", "result": result }