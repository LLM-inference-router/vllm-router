from kubernetes import client, config

# Load kubeconfig
config.load_config()

# Define the namespace and labels to filter
namespace = "default"  
labels_filter = "app=myapp" 

def list_services(namespace, label_filter, additional_labels):
    v1 = client.CoreV1Api()
    services_info = []

    # List services with the given label filter
    services = v1.list_namespaced_service(namespace=namespace, label_selector=label_filter)

    for svc in services.items:
        fqdn = f"{svc.metadata.name}.{namespace}.svc.cluster.local"  # Assuming default DNS configuration
        ip_address = svc.spec.cluster_ip
        # Extracting port information
        ports = [{"port": port.port, "name": port.name} for port in svc.spec.ports]
        
        # Extract the values for the additional labels
        additional_labels_values = {label: svc.metadata.labels.get(label, "Not specified") for label in additional_labels}
        
        services_info.append({
            "fqdn": fqdn, 
            "ip": ip_address, 
            "ports": ports, 
            "additional_labels": additional_labels_values
        })

    return services_info

def list_services_for_labels(namespace, label_filters, additional_labels):
    all_services = []
    for label_filter in label_filters:
        services = list_services(namespace, label_filter, additional_labels)
        all_services.extend(services)  # Aggregate results from each label filter
    return all_services
