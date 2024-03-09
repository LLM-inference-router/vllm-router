# vLLM Router

vLLM Router is a centralized API gateway that provides a single entry point for routing requests to various 
[vLLM](https://docs.vllm.ai/en/latest/index.html) services. vLLM Router simplifies the process of
managing and accessing multiple vLLM models by abstracting away the complexities of individual service endpoints. It is
built using FastAPI and Uvicorn, ensuring high performance and scalability.

## Motivation

vLLM can be deployed as a server that implements the OpenAI API protocol, allowing it to be used as a drop-in
replacement for applications using the OpenAI API. 
[However, the current vLLM server hosts only one model at a time.](https://docs.vllm.ai/en/latest/getting_started/quickstart.html#openai-compatible-server:~:text=The%20server%20currently%20hosts%20one%20model%20at%20a%20time)
This limitation can be challenging when deploying multiple vLLM models, as it requires managing separate API endpoints
for each model.

vLLM Router addresses this challenge by providing a unified interface for accessing all the vLLM services. It acts as a
proxy, routing requests to the appropriate vLLM service based on the specified model.

By using vLLM Router, developers can easily integrate various vLLM models into their applications without worrying about
the underlying infrastructure. They can make API requests to the vLLM Router, specifying the desired model, and the
router will handle the routing to the appropriate vLLM service.

## Features

- Single entry point for accessing multiple vLLM services
- Dynamic routing based on model name
- Seamless integration with Kubernetes using Helm for easy deployment and scaling
- Built using FastAPI and Uvicorn for high performance and scalability
- Simplifies the management and usage of vLLM models in applications

## Architecture

The vLLM Router consists of the following components:

1. FastAPI Application: The core of the vLLM Router is a FastAPI application that exposes API endpoints for handling
   incoming requests. It receives requests from clients and routes them to the appropriate vLLM service based on the
   specified model.

2. Kubernetes Integration: vLLM Router is designed to work seamlessly with Kubernetes. It leverages Kubernetes' service
   discovery mechanism to route requests to the vLLM services running within the cluster.

3. Configuration: The vLLM Router reads the model configuration from environment variables, which are set based on the
   values defined in the Helm chart's `values.yaml` file. This allows for easy configuration and updates without
   modifying the router's code.

## Installation

### Prerequisites

- Kubernetes cluster
- Helm (version 3+)
- Docker

### Deployment

1. Clone the vLLM Router repository:

   ```bash
   git clone https://github.com/yourusername/vllm-router.git
   ```

2. Build the vLLM Router Docker image:

   ```bash
   cd vllm-router
   docker build -t quay.io/llm_router/vllm-router:latest .
   docker push
   ```

   If you want to push the image to a different registry, update the `router.image` value in the `values.yaml` file.

3. Deploy the vLLM Router using Helm:

   ```bash
   cd vllm-chart
   ```

   Update the `values.yaml` file with the desired configuration for your vLLM models and the vLLM Router.

   Install the Helm chart:

   ```bash
   helm install vllm-router .
   ```

   This command will deploy the vLLM Router and the configured vLLM models in your Kubernetes cluster.

4. Access the vLLM Router:

   ```bash
   kubectl port-forward service/vllm-router 8000:8000
   ```

   The vLLM Router will be accessible at `http://localhost:8000`.

## Usage

To use the vLLM Router, make API requests to the following endpoint:

```
http://localhost:8000/v1/completions
```

Include the desired model in the request payload, and the vLLM Router will route the request to the appropriate vLLM
service based on the model name.

Example requests:

```bash
curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{ "prompt": "San Francisco is a", 
"model": "TheBloke/Llama-2-13B-chat-GPTQ", "max_tokens": 30, "temperature": 1}'
```

```bash
curl http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{ "prompt": "San Francisco is a", 
"model": "meta-llama/Llama-2-7B-chat-hf", "max_tokens": 30, "temperature": 1}'
```

## Configuration

The vLLM Router and the vLLM models can be configured using the `values.yaml` file in the Helm chart. Update the file to
specify the desired models, their resources, and other configuration options.

Refer to the `values.yaml` file for more information on the available configuration options.

## Contributing

Contributions to the vLLM Router project are welcome! If you find any issues or have suggestions for improvements,
please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [Apache-2.0 license](LICENSE).