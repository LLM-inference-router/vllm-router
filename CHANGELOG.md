# Changelog

All notable changes to the vLLM Router project will be documented in this file.

## [0.0.2] - 2024-03-09

### Added
- Helm chart for deploying vLLM Router and vLLM models in a Kubernetes cluster.
- `values.yaml` file for centralized configuration of vLLM Router and vLLM models.
- `templates/vllm-deployment.yaml` for deploying vLLM model Deployments.
- `templates/vllm-router.yaml` for deploying the vLLM Router Deployment and Service.
- `templates/services.yaml` for creating Services and ServiceMonitors for vLLM models.
- `templates/rbac.yaml` for defining RBAC roles and bindings for vLLM Router.
- `templates/persistent-volume.yaml` and `templates/persistent-volume-claim.yaml` for configuring persistent storage.
- `templates/gpu-operator-rbac.yaml` and `templates/gpu-operator-service-monitor.yaml` for GPU Operator integration.
- `.dockerignore` to ignore the `vllm-chart` directory during the Docker build process.

### Changed
- Updated `router.py` to read model configurations from environment variables set by the Helm chart.
- Updated the README.md file to provide instructions for deploying vLLM Router using the Helm chart.

### Removed
- Removed the `kubernetes_helper.py` file as it's no longer needed with the Helm chart deployment.
- Removed the `vllm-router-config.yaml` file as the configuration is now managed through the `values.yaml` file.
- Removed `kubernetes_helper.py` file as it's no longer used.
- Removed `vllm-deployment.yaml` file as it's no longer used directly.
- Removed `vllm-router.yaml` file as it's no longer used directly.

### Fixed
- Fixed the issue with missing `---` separators between resources in the generated YAML files.

## [0.0.1] - 2024-03-08

### Added
- Initial release of vLLM Router.
- `router.py` containing the FastAPI application for routing requests to vLLM services.
- `kubernetes_helper.py` for retrieving vLLM service information from Kubernetes.
- Dockerfile for building the vLLM Router Docker image.
- `vllm-deployment.yaml` for deploying vLLM models in Kubernetes.
- `vllm-router.yaml` for deploying the vLLM Router in Kubernetes.
- README.md file with project overview and usage instructions.