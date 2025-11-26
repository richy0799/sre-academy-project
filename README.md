
# Proyecto: App con métricas en Kubernetes + Prometheus + Grafana + Alertmanager

## Prerrequisitos
- Docker/Podman
- kubectl
- helm
- Minikube (o k3d/AKS/EKS/GKE)

## Pasos rápidos
```bash
minikube start --cpus=4 --memory=6g
eval $(minikube -p minikube docker-env)
docker build -t demo-metrics-app:1.0 .

kubectl create ns monitoring || true
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring -f k8s/monitoring/values.yaml

kubectl apply -f k8s/app/service.yaml
kubectl apply -f k8s/app/deployment.yaml
kubectl apply -f k8s/app/servicemonitor.yaml

kubectl apply -f k8s/monitoring/prometheus-rules.yaml

# Port-forward
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80
kubectl -n monitoring port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090
kubectl -n monitoring port-forward svc/monitoring-kube-prometheus-alertmanager 9093:9093
```

## Endpoints locales
- Grafana: http://127.0.0.1:3000 (admin / admin123)
- Prometheus: http://127.0.0.1:9090
- Alertmanager: http://127.0.0.1:9093
