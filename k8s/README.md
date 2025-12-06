# Kubernetes Deployment Guide
#
# This file provides instructions for deploying to Kubernetes.
# Run these commands from the project root directory.

# Prerequisites:
# - Kubernetes cluster running (Rancher Desktop, minikube, etc.)
# - kubectl configured to connect to your cluster
# - Docker images built

# ==============================================================================
# BUILD DOCKER IMAGES
# ==============================================================================

# Build backend image
docker build -f Dockerfile.backend -t wizards-keep-backend:latest ./backend

# Build frontend image
docker build -f Dockerfile.frontend -t wizards-keep-frontend:latest .

# For Rancher Desktop, images are automatically available to Kubernetes

# ==============================================================================
# DEPLOY TO KUBERNETES
# ==============================================================================

# Apply all configurations
kubectl apply -f k8s/

# Or apply in specific order:
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/database-configmap.yaml
kubectl apply -f k8s/database-secret.yaml
kubectl apply -f k8s/database-pvc.yaml
kubectl apply -f k8s/database-deployment.yaml
kubectl apply -f k8s/database-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

# Wait for database to be ready
kubectl wait --for=condition=ready pod -l app=database -n wizards-keep --timeout=120s

# Initialize database
kubectl apply -f k8s/db-init-job.yaml

# ==============================================================================
# VERIFY DEPLOYMENT
# ==============================================================================

# Check all resources
kubectl get all -n wizards-keep

# Check pods
kubectl get pods -n wizards-keep

# Check services
kubectl get svc -n wizards-keep

# Check logs
kubectl logs -l app=backend -n wizards-keep
kubectl logs -l app=frontend -n wizards-keep

# ==============================================================================
# ACCESS THE APPLICATION
# ==============================================================================

# Get frontend service URL (LoadBalancer)
kubectl get svc frontend -n wizards-keep

# Port forward if LoadBalancer doesn't work
kubectl port-forward svc/frontend 8080:80 -n wizards-keep

# Then access: http://localhost:8080

# ==============================================================================
# TROUBLESHOOTING
# ==============================================================================

# Describe pod for detailed information
kubectl describe pod <pod-name> -n wizards-keep

# Get pod logs
kubectl logs <pod-name> -n wizards-keep

# Execute commands in pod
kubectl exec -it <pod-name> -n wizards-keep -- /bin/sh

# Check database initialization
kubectl logs job/db-init -n wizards-keep

# ==============================================================================
# CLEANUP
# ==============================================================================

# Delete all resources
kubectl delete namespace wizards-keep

# Or delete specific resources
kubectl delete -f k8s/
