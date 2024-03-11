from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
import httpx
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

app = FastAPI()

backend_servers = {}

@app.on_event("startup")
async def startup_event():
    models = os.environ.get("MODELS", "").split(",")
    for model in models:
        # remove \n from the begin and end of the string
        model = model.strip()
        if model:
            model_name, model_url = model.split("=")
            backend_servers[model_name] = model_url
    logger.info(f"Backend servers: {backend_servers}")

async def proxy(request):
    logger.info(f'Received GET request from {request.client.host}:{request.client.port}')
    json_body = await request.json()
    # don't timeout on read
    timeout = httpx.Timeout(10.0, connect=60.0, read=None, write=60.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        # parse the json_body and and get the "model" value
        model = json_body.get("model")
        if model is None:
            raise HTTPException(status_code=400, detail="Model is required")
        # choose the backend server based on the model value
        server = backend_servers.get(model)
        if server is None:
            raise HTTPException(status_code=400, detail="Invalid model")
        backend_url = server + request.url.path
        logger.info(f"backend_url: {backend_url} for model {model}")

        if request.method == "GET":
            response = await client.get(backend_url, params=request.query_params)
        elif request.method == "POST":
            response = await client.post(backend_url, params=request.query_params, json=json_body)
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")
        response.raise_for_status()

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.content,
        }

@app.get("/v1/completions")
async def get_completions(request: Request):
    logger.info("get_completions")
    response_data = await proxy(request)
    return Response(
        content=response_data["content"],
        media_type=response_data["headers"].get("Content-Type"),
        status_code=response_data["status_code"],
    )

@app.post("/v1/completions")
async def post_completions(request: Request):
    logger.info("post_completions")
    response_data = await proxy(request)
    return Response(
        content=response_data["content"],
        media_type=response_data["headers"].get("Content-Type"),
        status_code=response_data["status_code"],
    )

@app.get("/v1/chat/completions")
async def get_completions(request: Request):
    logger.info("get_completions")
    response_data = await proxy(request)
    return Response(
        content=response_data["content"],
        media_type=response_data["headers"].get("Content-Type"),
        status_code=response_data["status_code"],
    )

@app.post("/v1/chat/completions")
async def post_completions(request: Request):
    logger.info("post_completions")
    response_data = await proxy(request)
    return Response(
        content=response_data["content"],
        media_type=response_data["headers"].get("Content-Type"),
        status_code=response_data["status_code"],
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
