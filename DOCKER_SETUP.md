# Docker Setup Guide for Semantic Image Search

Complete guide to running the Semantic Image Search application (backend + frontend) using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- OpenAI API Key
- Qdrant Cloud Account (or local Qdrant instance)

## Quick Start

### 1. Setup Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key
QDRANT_URL=https://your-cluster.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=semantic_images

# Optional
LOG_LEVEL=INFO
```

### 2. Build and Start Services

Build and start both backend and frontend:

```bash
docker-compose up --build
```

Or run in detached mode (background):

```bash
docker-compose up -d --build
```

### 3. Access the Application

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend (Expo)**: http://localhost:19002
- **Health Check**: http://localhost:8000/health

## Service Architecture

```
┌─────────────────────────────────────────┐
│         Docker Network                  │
│  (semantic-search-network)              │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │◄───┤  Frontend    │  │
│  │   FastAPI    │    │  React Native│  │
│  │  Port: 8000  │    │  Port: 19002 │  │
│  └──────────────┘    └──────────────┘  │
│         │                               │
│         ▼                               │
│  ┌──────────────┐                      │
│  │   Volumes    │                      │
│  │  - temp_imgs │                      │
│  │  - results   │                      │
│  │  - data      │                      │
│  └──────────────┘                      │
└─────────────────────────────────────────┘
         │
         ▼
   External Services
   - Qdrant Cloud
   - OpenAI API
```

## Docker Commands

### Start Services

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Start specific service
docker-compose up backend
docker-compose up frontend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

### View Logs

```bash
# All services
docker-compose logs

# Follow logs (live)
docker-compose logs -f

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Service Status

```bash
# List running containers
docker-compose ps

# Check service health
docker-compose ps backend
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec backend bash

# Run Python in backend
docker-compose exec backend python -c "import torch; print(torch.__version__)"

# Frontend shell
docker-compose exec frontend sh

# NPM commands in frontend
docker-compose exec frontend npm install <package>
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

## Development Workflow

### Backend Development

The backend code is mounted as a volume, so changes are reflected immediately with hot reload:

```bash
# Edit files in semantic_image_search/backend/
# Changes auto-reload in container
docker-compose logs -f backend
```

### Frontend Development

Frontend code is also mounted, with Expo watching for changes:

```bash
# Edit files in mobile-app/
# Expo will reload automatically
docker-compose logs -f frontend
```

### Rebuild After Dependency Changes

If you modify `requirements.txt` or `package.json`:

```bash
# Rebuild specific service
docker-compose up -d --build backend
docker-compose up -d --build frontend

# Or rebuild all
docker-compose up -d --build
```

## Troubleshooting

### Backend Container Won't Start

**Problem**: Backend exits immediately or shows errors

**Solutions**:
```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Missing environment variables
cat .env  # Verify OPENAI_API_KEY, QDRANT_URL, etc.

# 2. Port already in use
lsof -ti:8000 | xargs kill -9  # Kill process on port 8000

# 3. Permission issues
sudo chown -R $USER:$USER temp_images saved_results data
```

### Frontend Container Issues

**Problem**: Expo not starting or showing connection errors

**Solutions**:
```bash
# Check logs
docker-compose logs frontend

# Rebuild node_modules
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# Restart with cache clear
docker-compose restart frontend
```

### Cannot Connect to Backend from Frontend

**Problem**: API calls failing with network errors

**Solutions**:

1. **Verify backend is healthy**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check Docker network**:
   ```bash
   docker network inspect semantic-search-network
   ```

3. **Update API URL in frontend**:
   - For Docker network: `http://backend:8000`
   - From host machine: `http://localhost:8000`
   - For physical device: `http://<your-ip>:8000`

### Port Conflicts

**Problem**: Port already in use

**Solutions**:
```bash
# Check what's using the port
lsof -i :8000
lsof -i :19002

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Maps host 8001 to container 8000
```

### Out of Disk Space

**Problem**: Docker consuming too much space

**Solutions**:
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Complete cleanup (careful!)
docker system prune -a --volumes

# Check disk usage
docker system df
```

### Backend Models Not Loading

**Problem**: CLIP model download fails or takes too long

**Solutions**:
```bash
# Pre-download models
docker-compose exec backend python -c "
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/clip-ViT-B-32')
print('Model loaded successfully')
"

# Check available disk space
docker-compose exec backend df -h

# Increase Docker resources in Docker Desktop settings
# Recommended: 4GB+ RAM, 2+ CPUs
```

## Production Deployment

### Security Considerations

1. **Use secrets management**:
   ```bash
   # Don't commit .env file
   # Use Docker secrets or external secret managers
   docker secret create openai_key ./openai_key.txt
   ```

2. **Update docker-compose for production**:
   ```yaml
   # Remove volume mounts for code
   # Use built images instead
   # Add resource limits
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 4G
   ```

3. **Enable HTTPS**:
   - Add nginx reverse proxy
   - Use Let's Encrypt for SSL certificates
   - Update CORS settings

### Environment-Specific Configs

Create multiple compose files:

```bash
# Development
docker-compose.yml

# Production
docker-compose.prod.yml

# Use specific config
docker-compose -f docker-compose.prod.yml up
```

### Health Monitoring

```bash
# Check service health
docker-compose ps

# Watch health status
watch docker-compose ps

# Set up monitoring (Prometheus, Grafana)
# Add health check endpoints
```

## Advanced Configuration

### Custom Network Configuration

```yaml
networks:
  semantic-search-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

### Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### Multiple Environments

```bash
# Development
docker-compose --env-file .env.dev up

# Staging
docker-compose --env-file .env.staging up

# Production
docker-compose --env-file .env.prod up
```

## Backup and Restore

### Backup Volumes

```bash
# Backup saved results
docker run --rm -v semantic-image-search_saved_results:/data -v $(pwd):/backup \
  alpine tar czf /backup/saved_results_backup.tar.gz -C /data .

# Backup temp images
docker run --rm -v semantic-image-search_temp_images:/data -v $(pwd):/backup \
  alpine tar czf /backup/temp_images_backup.tar.gz -C /data .
```

### Restore Volumes

```bash
# Restore saved results
docker run --rm -v semantic-image-search_saved_results:/data -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/saved_results_backup.tar.gz"
```

## Performance Optimization

### Image Size Reduction

```dockerfile
# Use multi-stage builds
FROM python:3.11-slim as builder
# Install dependencies
FROM python:3.11-slim
# Copy only necessary files
```

### Build Cache

```bash
# Use BuildKit for better caching
DOCKER_BUILDKIT=1 docker-compose build

# Layer caching
# Order Dockerfile commands from least to most frequently changed
```

### Resource Allocation

In Docker Desktop:
- **Memory**: 4GB minimum, 8GB recommended
- **CPUs**: 2 minimum, 4+ recommended
- **Disk**: 20GB+ for images and models

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Images
on:
  push:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build images
        run: docker-compose build
      - name: Run tests
        run: docker-compose up -d && docker-compose exec backend pytest
```

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify environment variables: `cat .env`
3. Test connectivity: `curl http://localhost:8000/health`
4. Review Docker resources: `docker system df`
5. Check network: `docker network inspect semantic-search-network`

## Cleanup

Complete cleanup when done:

```bash
# Stop and remove everything
docker-compose down -v --rmi all

# Remove networks
docker network prune

# Remove all unused resources
docker system prune -a --volumes
```
