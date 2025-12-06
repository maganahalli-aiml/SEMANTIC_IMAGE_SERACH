# 🚀 Quick Start Guide - Dockerized Semantic Image Search

## 1️⃣ One-Time Setup (5 minutes)

### Step 1: Configure Environment Variables
```bash
cd /path/to/SEMANTIC-IMAGE-SEARCH
cp .env.example .env
nano .env  # or use your favorite editor
```

Add your credentials:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
QDRANT_URL=https://your-cluster.aws.cloud.qdrant.io
QDRANT_API_KEY=your-actual-qdrant-key
QDRANT_COLLECTION_NAME=semantic_images
```

## 2️⃣ Start the Application

### Option A: Automated Script (Recommended)
```bash
./start-docker.sh
```
This checks prerequisites, builds images, and starts all services automatically.

### Option B: Manual Commands
```bash
# Build and start
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 3️⃣ Access Your Application

Once services are running:

| Service | URL | Description |
|---------|-----|-------------|
| **Backend API** | http://localhost:8000 | REST API endpoints |
| **API Documentation** | http://localhost:8000/docs | Interactive Swagger UI |
| **Frontend App** | http://localhost:19002 | Expo development server |
| **Health Check** | http://localhost:8000/health | Backend status |

## 4️⃣ Test the Application

### Test Backend (Terminal)
```bash
# Health check
curl http://localhost:8000/health | python3 -m json.tool

# Collection info
curl http://localhost:8000/collections/info | python3 -m json.tool

# Text search
curl -X POST http://localhost:8000/search/text \
  -H "Content-Type: application/json" \
  -d '{"query_text": "red flowers", "k": 5}'
```

### Test Frontend (Mobile/Simulator)

**For iOS Simulator:**
1. Open http://localhost:19002 in browser
2. Press `i` to open iOS simulator
3. Grant permissions when prompted
4. Try text search: "yellow flowers"

**For Android Emulator:**
1. Open http://localhost:19002 in browser
2. Press `a` to open Android emulator
3. Update API URL in `mobile-app/services/api.js` to `http://10.0.2.2:8000`

**For Physical Device:**
1. Install Expo Go app from App Store/Play Store
2. Scan QR code from http://localhost:19002
3. Update API URL in `mobile-app/services/api.js` to your computer's IP
4. Find IP: `ifconfig | grep "inet " | grep -v 127.0.0.1`

## 5️⃣ Common Commands

Use the helper script for common tasks:

```bash
# Show all available commands
./docker-commands.sh help

# Quick commands
./docker-commands.sh start      # Start all services
./docker-commands.sh stop       # Stop all services
./docker-commands.sh logs       # View all logs
./docker-commands.sh logs-api   # View backend logs only
./docker-commands.sh logs-app   # View frontend logs only
./docker-commands.sh status     # Check service status
./docker-commands.sh restart    # Restart services
./docker-commands.sh test       # Test API connectivity
```

## 6️⃣ Development Workflow

### Backend Development
```bash
# Edit files in semantic_image_search/backend/
# Changes auto-reload (uvicorn --reload enabled)

# View logs
docker-compose logs -f backend

# Access container shell
docker-compose exec backend bash

# Run Python commands
docker-compose exec backend python -c "import torch; print(torch.__version__)"
```

### Frontend Development
```bash
# Edit files in mobile-app/
# Expo watches for changes and reloads

# View logs
docker-compose logs -f frontend

# Access container shell
docker-compose exec frontend sh

# Install new npm package
docker-compose exec frontend npm install <package-name>
```

### After Dependency Changes
```bash
# Backend (requirements.txt changed)
docker-compose up -d --build backend

# Frontend (package.json changed)
docker-compose up -d --build frontend
```

## 7️⃣ Stopping the Application

```bash
# Stop services (keeps data)
docker-compose down

# Stop and remove volumes (cleans everything)
docker-compose down -v

# Complete cleanup (removes images too)
docker-compose down -v --rmi all
```

## 8️⃣ Troubleshooting

### Backend Won't Start
```bash
# Check logs
docker-compose logs backend

# Common fixes:
# 1. Verify .env file has correct values
cat .env

# 2. Kill processes on port 8000
lsof -ti:8000 | xargs kill -9

# 3. Rebuild without cache
docker-compose build --no-cache backend
```

### Frontend Connection Issues
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify API URL in services/api.js
# iOS Simulator: http://localhost:8000
# Android Emulator: http://10.0.2.2:8000
# Physical Device: http://YOUR_IP:8000

# Restart frontend
docker-compose restart frontend
```

### Port Conflicts
```bash
# Check what's using ports
lsof -i :8000    # Backend
lsof -i :19002   # Frontend

# Change ports in docker-compose.yml if needed
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

### Out of Space
```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a --volumes
```

## 9️⃣ API Examples

### Text Search
```bash
curl -X POST http://localhost:8000/search/text \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "yellow flowers in bloom",
    "k": 10,
    "metadata_filter": {"category": "flower"},
    "save_results": false
  }'
```

### Image Search
```bash
curl -X POST http://localhost:8000/search/image \
  -F "image=@/path/to/image.jpg" \
  -F "k=10" \
  -F 'metadata_filter={"category": "flower"}' \
  -F "save_results=false"
```

### Get Categories
```bash
curl http://localhost:8000/metadata/categories
```

## 🔟 Production Deployment

For production deployment:

1. **Update docker-compose.yml**:
   - Remove volume mounts
   - Add resource limits
   - Change restart policy

2. **Security**:
   - Use Docker secrets for API keys
   - Enable HTTPS with nginx
   - Update CORS settings

3. **Monitoring**:
   - Add health check endpoints
   - Set up logging aggregation
   - Configure alerts

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed production configuration.

---

## 📚 Additional Resources

- **Backend API**: http://localhost:8000/docs
- **Mobile App README**: [mobile-app/README.md](mobile-app/README.md)
- **Docker Guide**: [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Main README**: [README.md](README.md)

## 🆘 Get Help

- Check logs: `docker-compose logs -f`
- Test connectivity: `./docker-commands.sh test`
- Restart services: `./docker-commands.sh restart`
- Full documentation: [DOCKER_SETUP.md](DOCKER_SETUP.md)

---

**Need help?** Open an issue on GitHub or check the troubleshooting section in DOCKER_SETUP.md

**Happy Searching!** 🔍✨
