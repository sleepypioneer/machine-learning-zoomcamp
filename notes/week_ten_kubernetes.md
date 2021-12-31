# Kubernetes and Tensor Flow Serving

TF-serving is C++ library that focuses on inference. It takes the prepared X matrix and returns the predictions.
We will build a gateway service (in Flask) which can take a URL collect the image and do the necessary transformation for preprocessing. The gateway will then send the X matrix to the TF-serving, take the returned predictions (using grpc protocol) and use them to return predictions to the user.


The whole architecture will live inside kubernetes. While TF-serving uses GPU our gateway service will use CPU. They can be scaled independantly.

### Save the model

```python
import tensorflow as tf
from tensorflow import keras


model = keras.models.load_model('./clothing-model-v4.h5')
tf.saved_model.save(model, 'clothing-model')
# creates folder for the model
```

```sh
# inspect what is in the model's folders
ls -lhR clothing-model

# inspect model
saved_model_cli show --dir clothing-model
```

### Running the TF-server and Gateway in Docker in one Network with Docker Compose

Docker-compose allows us to run instances of both the TF-server and our Gateway in the same network so they can access each other.

#### image-gateway.dockerfile

```dockerfile
FROM python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["gateway.py", "proto.py", "./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "gateway:app"]
```

#### image-gateway.dockerfile

```dockerfile
FROM tensorflow/serving:2.7.0

COPY clothing-model /models/clothing-model/1
ENV MODEL_NAME="clothing-model"
```

#### Docker compose file to run them together locally

```yaml
version: "3.9"
services:
  clothing-model:
    image: zoomcamp-10-model:xception-v4-001
  gateway:
    image: zoomcamp-10-gateway:002
    environment:
      - TF_SERVING_HOST=clothing-model:8500
    ports:
      - "9696:9696"
```

### Running in Kubernetes locally with Kind

** we need to use a specific tag for this to work (not lastest) ***

```sh
go install sigs.k8s.io/kind@v0.11.1 && kind create cluster

# delete cluster
kind delete cluster

# check cluster info
kubectl cluster-info --context kind-kind
```


#### Create deployment

Create a `deployment.yaml`, kubernetes extension will help fill this in.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ping
spec:
  selector:
    matchLabels:
      app: ping
  template:
    metadata:
      labels:
        app: ping
    spec:
      containers:
      - name: ping
        image: ping:v001
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
        ports:
        - containerPort: 9696
```

```sh
kubectl apply -f deployment.yaml

kubectl get deployment
kubectl get pods
kubectl describe deployment ping
```

#### Loading image into cluster

```sh
kind load docker-image ping:v001
```

#### Test deployment with port forwarding

```sh
kubectl port-forward service/ping 9696:9696

curl localhost:9696/ping
```

#### Create service

Create a `service.yaml`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ping
spec:
  selector:
    app: ping
  ports:
  - port: 80
    targetPort: 9696
```

targetPort == port for the pod
port == service port (ie 80)

ClusterIP == internal

Loadbalancer == external

In Kind as its local kubernets external ip will always be pending unless we configure it otherwise.

#### Environment variables

Pass through `env` in yaml

```yaml
containers:
    env:
        - name: TF_SERVING_HOST
            value: <NAME>.default:<PORT>
```

** watch out for loadbalancing with gRPC in kubernetes - can be tricky

### Deploying to EKS

Using [EKS cli](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html). **This costs money to run.**

Create EKS config file

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: mlzoomcamp-eks
  region: eu-west-1

nodeGroups:
  - name: ng-m5-xlarge
    instanceType: m5.xlarge
    desiredCapacity: 1
```

```sh
aws ecr create-repository --repository-name mlzoomcamp-images

ACCOUNT_ID=387546586013
REGION=eu-west-1
REGISTRY_NAME=mlzoomcamp-images
PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}

GATEWAY_LOCAL=zoomcamp-10-gateway:002
GATEWAY_REMOTE=${PREFIX}:zoomcamp-10-gateway-002
docker tag ${GATEWAY_LOCAL} ${GATEWAY_REMOTE}


MODEL_LOCAL=zoomcamp-10-model:xception-v4-001
MODEL_REMOTE=${PREFIX}:zoomcamp-10-model-xception-v4-001
docker tag ${MODEL_LOCAL} ${MODEL_REMOTE}

aws ecr get-login --no-include-email

docker push ${MODEL_REMOTE}
docker push ${GATEWAY_REMOTE}
```

Find the remote image we have just created and replace it in the config files.

```sh
eksctl create cluster -f eks-config.yaml
```

Once this is created (it can take some time) you can then apply the config to create the deployments and services.

```sh
kubectl apply -f gateway-deployment.yaml
kubectl apply -f gateway-service.yaml

#find the external IP
kubectl get service

# will be a long url that has region.elb.amazon.com within it.
```

Don't forget to also remove the instance you created!! To delete it:

```sh
eksctl delete cluster --name mlzoomcamp-eks
```

For production you would also need to ensure that the endpoints are not public and have some sort of security is in place.


## Explore more

- Other local Kuberneteses: minikube, k3d, k3s, microk8s, EKS Anywhere
- Rancher desktop
- Docker desktop
- Lens
- Many cloud providers have Kubernetes: GCP, Azure, Digital ocean and others. Look for "Managed Kubernetes" in your favourite search engine
- Deploy the model from previous modules and from your project with Kubernetes
- Learn about Kubernetes namespaces. Here we used the default namespace