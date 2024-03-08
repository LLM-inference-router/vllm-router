from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from http import HTTPStatus
import httpx
import logging
from kubernetes_helper import list_services_for_labels

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

app = FastAPI()

#    "TheBloke/Llama-2-13B-chat-GPTQ": "http://10.104.125.148:8000",
#    "TheBloke/Llama-2-7B-chat-GPTQ": "http://10.97.24.66:8000",

# Define the namespace
namespace = "default"  # Namespace to query

# Define label filters
label_filters = ["app=vllm-llama-7b-gptq", "app=vllm-llama-13b-gptq", "app=vllm-llama-7b"]
model_label = "model_name"
model_family_label="model_family"
# define the services and model mapping
backend_servers = {}



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

if __name__ == "__main__":
    import uvicorn
    # add to backend_servers
    servers = list_services_for_labels(namespace, label_filters, additional_labels=[model_label, model_family_label])
    for server in servers:
        # use model_name and model_family labels as key and IP and port as value in the backend_servers dictionary
        key = server["additional_labels"][model_family_label] + "/" + server["additional_labels"][model_label]
        value = "http://" + server["ip"] + ":8000"
        backend_servers[key] = value
    logger.info(f"backend_servers: {backend_servers}")

    uvicorn.run(app, host="127.0.0.1", port=8000)
