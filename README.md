# vllm-router
vLLM Router is to provide single point of entry to route to all the vLLM services. It is a simple RESTful API server that listens to the incoming requests and routes them to the appropriate vLLM service. It is built using FastAPI and Uvicorn.

## Installation in Kubernetes

### Prerequisites
Make sure all the vLLM Services are labeled with `model_name` and `model_family` so that the vLLM Router can route the requests to the appropriate service.
`model_family` is the Huggingface organizatin of the model, e.g. `meta-llama` and `model_name` is the name of the model, e.g. `Llama-2-7B-chat-hf`. 
Make sure the `model_family` and `model_name` match the model used by the vLLM deployment.

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: vllm-llama-7b
    model_family: meta-llama
    model_name: Llama-2-7B-chat-hf

```

### Create vLLM Router

Update the `ConfigMap` in the `vllm-router.yaml` file with the appropriate values, so that vLLM router can filter the services based on the labels.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vllm-router-config
  namespace: default
data:
  label_filters.txt: |
    app=vllm-llama-7b-gptq
    app=vllm-llama-13b-gptq
    app=vllm-llama-7b
```

To install the vLLM Router in Kubernetes, you can use the following command:
```bash
kubectl apply -f vllm-router.yaml
```
