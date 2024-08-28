# Table of content
1. Development lifecycle
2. Deployment lifecycle
3. Debug deployment
4. Setup mulesoft Flexgateway on Mac (M1 ARM)


```sequenceDiagram
    actor User
    participant FastAPI
    participant Kafka
    participant PythonConsumer
    participant Salesforce

    User->>FastAPI: Send request
    FastAPI->>Kafka: Send message
    Kafka->>PythonConsumer: Consume message
    PythonConsumer->>Salesforce: Update or create contacts
    Salesforce-->>PythonConsumer: Confirm action
    FastAPI-->>User: Send response
```

# Deployment Lifecycle

Step 1: Build the image locally

```bash
docker build -t my-fastapi-app:latest .
```

2. Start Minikube Docker Environment

```bash
minikube start
```

3. Get the name of minikube profile

```bash
|-------------|-----------|---------|--------------|------|---------|---------|-------|--------|
|   Profile   | VM Driver | Runtime |      IP      | Port | Version | Status  | Nodes | Active |
|-------------|-----------|---------|--------------|------|---------|---------|-------|--------|
| mq-minikube | docker    | docker  | 192.168.49.2 | 8443 | v1.23.6 | Running |     1 | *      |
|-------------|-----------|---------|--------------|------|---------|---------|-------|--------|
```

4. Configure your Docker environment to use Minikube’s Docker daemon
<center> eval $(minikube -p PROFILE_NAME docker-env)</center>

```bash
eval $(minikube -p mq-minikube docker-env)
```


Step 5: Re-Build the image in minikube docker demon
```bash
docker build -t my-fastapi-app:latest .

docker  images
```

6. Use the Image in Your Minikube Kubernetes Deployment
   <br/> a) deployment.yaml
   <br/> b) service.yaml

```yaml
# deployment.yaml
apiVersion: apps/v1  # Specifies the API version used for the deployment
kind: Deployment  # Defines the type of Kubernetes resource, in this case, a Deployment
metadata:
  name: my-fastapi-app-deployment  # The name of the Deployment resource a.k.a your build image name
spec:
  replicas: 1  # Number of pod replicas to run; in this case, only 1 pod will be running
  selector:
    matchLabels:
      app: my-fastapi-app  # Label selector used to identify the pods that this Deployment will manage
  template:
    metadata:
      labels:
        app: my-fastapi-app  # Labels applied to the pods created by this Deployment
    spec:
      containers:
      - name: my-fastapi-app  # Name of the container within the pod
        image: my-fastapi-app:latest  # The Docker image to use for this container
        imagePullPolicy: Never  # Ensures Kubernetes uses the locally built image without pulling from a registry
        ports:
        - containerPort: 8000  # The port that the container exposes internally
        resources:
          limits:
            memory: "128Mi"  # Maximum memory the container can use
            cpu: "200m"  # Maximum CPU the container can use (200 milliCPU)


```

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-fastapi-app-service
spec:
  type: NodePort  # Exposes the service on a specific port on each node
  selector:
    app: my-fastapi-app
  ports:
  - protocol: TCP
    port: 80  # The port that will be exposed outside the cluster
    targetPort: 8000  # The port your FastAPI app listens to inside the container
    nodePort: 30007  # You can specify a port or let Kubernetes assign one (30000-32767)


```

```bash
$ kubectl apply -f kubernetes/base/
```

7. Deploy to Minikube

```bash
kubectl apply -f deployment.yaml
```

```bash
kubectl apply -f service.yaml
```

8. Verify the Pod is Running

```bash
kubectl get pods
```

9. Verify the Pod and service is Running

```bash
kubectl get pods
```

```bash
kubectl get services
```
10. Start the application
    <br/> a) In console
    ```bash
    minikube service my-fastapi-app-service
    ```
    <br/> b) In detach mode inside console

    ```bash
    minikube service my-fastapi-app-service --url &
    ```
### 3. Debug Deployment

Here's the handful of command to debug the deployment on minikube

```bash
$ kubectl get namespaces

$ kubectl get services

$ kubectl get pods

$ kubectl describe pod <POD_NAME>

$ kubectl logs <POD_NAME>

$ kubectl delete deployment my-fastapi-app-deployment

$ kubectl delete service my-fastapi-app-service

$ kubectl apply -f deployment.yaml

$ kubectl apply -f service.yaml
```

### 4. How to configure Mulesoft FlexGateway on Mac M1

A. Cleanup Kubernetes Resources

```bash
helm -n gateway uninstall ingress
```

```bash
kubectl delete namespace gateway
```

```bash
eval $(minikube -p mq-minikube docker-env)
```

```bash
docker rmi -f mulesoft/flex-gateway:1.8.0-amd64
docker rmi -f mulesoft/flex-gateway:1.8.0
docker rmi -f mulesoft/flex-gateway:latest
```

```bash
minikube stop
minikube start
```

```bash
docker pull --platform linux/amd64 mulesoft/flex-gateway:1.8.0
docker tag mulesoft/flex-gateway:1.8.0 mulesoft/flex-gateway:1.8.0-amd64
```

```bash
docker run --entrypoint flexctl -u $UID \
  -v "$(pwd)":/registration mulesoft/flex-gateway \
  registration create --organization=500af473-a7b6-4fac-8e8e-95a7596659ab \
  --token=90e6e4bb-a2bd-4da6-a658-96bd15cff1ea \
  --output-directory=/registration \
  --connected=true \
  PUT_YOUR_OWN_GATEWAY_NAME_HERE
```

```bash
helm repo add flex-gateway https://flex-packages.anypoint.mulesoft.com/helm
helm repo update
```

```bash
helm -n gateway upgrade -i --create-namespace --wait ingress flex-gateway/flex-gateway \
  --set-file registration.content=registration.yaml \
  --set gateway.mode=connected \
  --set image.repository=mulesoft/flex-gateway \
  --set image.tag=1.8.0-amd64
```

```bash
kubectl get pods -n gateway
```

```bash
kubectl get svc ingress -o yaml -n gateway
```

```bash
 minikube service ingress -n gateway
```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```


```bash
1228  helm -n gateway uninstall ingress\n
 1229  kubectl delete namespace gateway\n
 1230  docker rmi mulesoft/flex-gateway:1.8.0-amd64\ndocker rmi mulesoft/flex-gateway:1.8.0\ndocker rmi mulesoft/flex-gateway:latest\n
 1231  docker rmi -f mulesoft/flex-gateway:1.8.0-amd64\ndocker rmi -f mulesoft/flex-gateway:1.8.0\ndocker rmi -f mulesoft/flex-gateway:latest\n
 1232  minikube stop
 1233  minikube start
 1234  docker images
 1235  eval $(minikube -p mq-minikube docker-env)\n
 1236  docker images
 1237  docker pull --platform linux/amd64 mulesoft/flex-gateway:1.8.0
 1238  docker tag mulesoft/flex-gateway:1.8.0 mulesoft/flex-gateway:1.8.0-amd64
 1239  docker images
 1240  helm repo add flex-gateway https://flex-packages.anypoint.mulesoft.com/helm
 1241  helm -n gateway upgrade -i --create-namespace --wait ingress flex-gateway/flex-gateway \\n  --set-file registration.content=registration.yaml \\n  --set gateway.mode=connected \\n  --set image.repository=mulesoft/flex-gateway \\n  --set image.tag=1.8.0-amd64\n
(.venv) (base) mq10006848@ITS-FVFL21EX1WG7 gateway-kube-mini-test2 % 

```
