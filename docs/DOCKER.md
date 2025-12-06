# Docker & Containerization Guide

## What is Docker?

Docker is a platform that packages applications and their dependencies into **containers** - lightweight, portable units that run consistently across different environments.

## Why Containerization?

### The Problem
"It works on my machine!" - Every developer has said this.

Traditional deployment challenges:
- Different OS versions
- Different installed libraries
- Different configurations
- Environment inconsistencies

### The Solution
Containers package everything together:
- Your application code
- Runtime environment (Python, Node.js, etc.)
- System libraries
- Dependencies
- Configuration

Result: **Runs the same everywhere**

## Docker Concepts

### Images
A Docker **image** is a blueprint for containers. Like a cookie cutter.

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim          # Start with Python 3.11
COPY . /app                    # Copy application code
RUN pip install -r requirements.txt  # Install dependencies
CMD ["python", "main.py"]      # Run the application
```

Build an image:
```powershell
docker build -f Dockerfile.backend -t wizards-keep-backend .
```

### Containers
A **container** is a running instance of an image. Like a cookie.

```powershell
# Run a container from an image
docker run -p 8000:8000 wizards-keep-backend
```

Multiple containers from one image:
```powershell
docker run -p 8001:8000 --name backend1 wizards-keep-backend
docker run -p 8002:8000 --name backend2 wizards-keep-backend
```

### Volumes
**Volumes** persist data beyond container lifetime.

```powershell
# Without volume: data lost when container stops
docker run postgres:15

# With volume: data persists
docker run -v postgres-data:/var/lib/postgresql/data postgres:15
```

### Networks
**Networks** allow containers to communicate.

```powershell
# Create network
docker network create wizards-network

# Run containers on same network
docker run --network wizards-network --name db postgres:15
docker run --network wizards-network --name api my-backend
```

Backend can now connect to database at `db:5432` (using container name as hostname!)

## The Wizard's Keep Dockerfiles

### Backend Dockerfile

```dockerfile
# Multi-stage build for smaller final image

# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Copy only what's needed
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local  # Copy installed packages
COPY . .  # Copy application code
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why multi-stage?**
- Builder stage has compilers and build tools (large!)
- Runtime stage only has what's needed to run (small!)
- Final image is 50% smaller

### Frontend Dockerfile

```dockerfile
FROM nginx:alpine
COPY frontend/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Simple and efficient:**
- Uses nginx to serve static files
- Alpine Linux base (tiny!)
- Production-ready

## Docker Compose

Docker Compose orchestrates multiple containers.

### The Problem
Running each service manually:
```powershell
docker run -d --name db postgres:15
docker run -d --name backend my-backend
docker run -d --name frontend my-frontend
```

Tedious and error-prone!

### The Solution
One file describes all services:

```yaml
# docker-compose.yml
version: '3.8'

services:
  database:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: wizard123
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  backend:
    build: ./backend
    depends_on:
      - database
    environment:
      DATABASE_URL: postgresql://wizard:wizard123@database:5432/wizards_keep
  
  frontend:
    build: ./frontend
    ports:
      - "8080:80"
    depends_on:
      - backend

volumes:
  postgres-data:
```

Start everything:
```powershell
docker-compose up -d
```

Stop everything:
```powershell
docker-compose down
```

## Common Docker Commands

### Images
```powershell
# List images
docker images

# Build image
docker build -t my-image:latest .

# Remove image
docker rmi my-image:latest

# Pull image from registry
docker pull postgres:15
```

### Containers
```powershell
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Start container
docker start my-container

# Stop container
docker stop my-container

# Remove container
docker rm my-container

# View logs
docker logs my-container

# Execute command in container
docker exec -it my-container /bin/bash
```

### System
```powershell
# View disk usage
docker system df

# Clean up unused resources
docker system prune -a

# View container resource usage
docker stats
```

## Best Practices

### 1. Use Specific Image Tags
```dockerfile
# BAD: Could pull different versions
FROM python:latest

# GOOD: Predictable and reproducible
FROM python:3.11-slim
```

### 2. Minimize Layers
```dockerfile
# BAD: Each RUN creates a layer
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2

# GOOD: One layer
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### 3. Use .dockerignore
```
# .dockerignore
__pycache__/
*.pyc
.git/
.env
venv/
node_modules/
```

Prevents copying unnecessary files into images.

### 4. Run as Non-Root User
```dockerfile
# Create and use non-root user
RUN useradd -m -u 1000 appuser
USER appuser
```

Security best practice!

### 5. Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

Allows orchestrators to detect if container is healthy.

## Development vs Production

### Development
```yaml
services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app  # Mount source code
    environment:
      DEBUG: "true"
    command: uvicorn app.main:app --reload  # Auto-reload on changes
```

**Benefits:**
- Hot reload (changes reflected immediately)
- Easy debugging
- Fast iteration

### Production
```dockerfile
FROM python:3.11-slim
COPY . /app  # Copy code into image
ENV DEBUG="false"
USER appuser
CMD ["uvicorn", "app.main:app"]  # No reload
```

**Benefits:**
- Immutable (same image everywhere)
- Smaller attack surface
- Better performance

## Troubleshooting

### Container Won't Start
```powershell
# Check logs
docker logs my-container

# Check if port is already in use
netstat -ano | findstr :8000
```

### Can't Connect to Container
```powershell
# Verify port mapping
docker ps  # Look at PORTS column

# Test from inside container
docker exec -it my-container curl http://localhost:8000
```

### Out of Disk Space
```powershell
# See what's using space
docker system df

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Nuclear option: clean everything
docker system prune -a --volumes
```

### Container Performance Issues
```powershell
# Check resource usage
docker stats

# Limit resources
docker run -m 512m --cpus="1.0" my-image
```

## Building for The Wizard's Keep

### Local Development
```powershell
# Build images
docker build -f Dockerfile.backend -t wizards-keep-backend ./backend
docker build -f Dockerfile.frontend -t wizards-keep-frontend .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### For Kubernetes
```powershell
# Build and tag for registry
docker build -f Dockerfile.backend -t myregistry/wizards-keep-backend:v1.0 ./backend

# Push to registry
docker push myregistry/wizards-keep-backend:v1.0

# Kubernetes will pull from registry
kubectl apply -f k8s/
```

## Key Takeaways

1. **Containers solve "works on my machine"** - Same environment everywhere
2. **Images are blueprints, containers are running instances**
3. **Docker Compose orchestrates multi-container apps**
4. **Volumes persist data, networks connect containers**
5. **Multi-stage builds reduce image size**
6. **Use specific tags, not `latest`**
7. **Run as non-root for security**
8. **Development and production configs differ**

## Next Steps

After mastering Docker:
1. Learn Kubernetes for orchestration at scale
2. Explore container registries (Docker Hub, ECR, GCR)
3. Study CI/CD pipelines with containers
4. Learn about service meshes (Istio, Linkerd)

Docker is the foundation of modern DevOps!
