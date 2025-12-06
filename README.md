# Semantic Image Search System

A full-stack semantic image search application powered by CLIP embeddings, Qdrant vector database, and OpenAI. Search for images using natural language descriptions or by uploading similar images. Includes both FastAPI backend and React Native mobile app.

## 🌟 Features

### Backend (FastAPI)
- 🔍 **Text-to-Image Search**: Find images using natural language queries
- 📷 **Image-to-Image Search**: Upload an image to find visually similar images
- 🏷️ **Metadata Filtering**: Filter results by category, year, verified status, etc.
- 💾 **Result Management**: Save and retrieve search results
- 📊 **Collection Analytics**: View indexed image statistics
- 🚀 **High Performance**: Vector similarity search with Qdrant
- 🔒 **Production Ready**: Health checks, error handling, CORS enabled

### Frontend (React Native)
- 📱 **Cross-Platform**: iOS, Android, and Web support via Expo
- 🎨 **Material Design**: Beautiful UI with react-native-paper
- 📸 **Camera Integration**: Take photos or choose from gallery
- 🔎 **Real-time Search**: Instant results with similarity scores
- 📊 **Dashboard**: Backend health and collection statistics
- 🏷️ **Category Filters**: Filter by image categories

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│          React Native Mobile App            │
│     (iOS, Android, Web via Expo)            │
│                                             │
│  Home │ Text Search │ Image Search         │
└───────────────┬─────────────────────────────┘
                │
                │ HTTP/REST API
                ▼
┌───────────────────────────────────────────────┐
│           FastAPI Backend                     │
│                                               │
│  ┌─────────────────────────────────────┐    │
│  │  Routes                              │    │
│  │  /health  /search  /collections      │    │
│  └─────────────────────────────────────┘    │
│                    ▼                          │
│  ┌─────────────────────────────────────┐    │
│  │  Services                            │    │
│  │  • Image Processing                  │    │
│  │  • Embedding Generation (CLIP)       │    │
│  │  • Query Translation (GPT-4o)        │    │
│  └─────────────────────────────────────┘    │
│                    ▼                          │
│  ┌─────────────────────────────────────┐    │
│  │  Vector Store (Qdrant)               │    │
│  │  • 512-dim CLIP embeddings           │    │
│  │  • Cosine similarity search          │    │
│  │  • Metadata filtering                │    │
│  └─────────────────────────────────────┘    │
└───────────────────────────────────────────────┘
```

## 🚀 Quick Start with Docker (Recommended)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- OpenAI API Key
- Qdrant Cloud Account

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SEMANTIC-IMAGE-SEARCH
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start the application**:
   ```bash
   ./start-docker.sh
   ```

   Or manually:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Frontend: http://localhost:19002
   - Health: http://localhost:8000/health

### Docker Management

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after changes
docker-compose up --build
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker documentation.

## 💻 Local Development Setup

### Backend Setup

#### Prerequisites
- Python 3.11+
- OpenAI API Key
- Qdrant Cloud Account

#### Installation

1. **Create virtual environment**:
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create `.env` file:
   ```bash
   OPENAI_API_KEY=your_key_here
   QDRANT_URL=https://your-cluster.aws.cloud.qdrant.io
   QDRANT_API_KEY=your_qdrant_key
   QDRANT_COLLECTION_NAME=semantic_images
   ```

4. **Run the backend**:
   ```bash
   ./run_api.sh
   # Or manually:
   # uvicorn semantic_image_search.backend.api_main:app --reload
   ```

5. **Access API**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

### Frontend Setup

#### Prerequisites
- Node.js 16+
- npm or yarn
- Expo CLI: `npm install -g expo-cli`

#### Installation

1. **Navigate to mobile app**:
   ```bash
   cd mobile-app
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure API URL** in `services/api.js`:
   ```javascript
   // For iOS Simulator
   const API_BASE_URL = 'http://localhost:8000';
   
   // For Android Emulator
   const API_BASE_URL = 'http://10.0.2.2:8000';
   
   // For Physical Device
   const API_BASE_URL = 'http://YOUR_IP:8000';
   ```

4. **Start Expo**:
   ```bash
   npm start
   ```

5. **Run on platform**:
   - Press `i` for iOS
   - Press `a` for Android
   - Scan QR with Expo Go app

See [mobile-app/README.md](mobile-app/README.md) for detailed frontend documentation.

## 📚 API Documentation

### Endpoints

#### Health Check
```bash
GET /health
```
Returns backend status and configuration.

#### Text-to-Image Search
```bash
POST /search/text
Content-Type: application/json

{
  "query_text": "red flowers in bloom",
  "k": 10,
  "metadata_filter": {"category": "flower"},
  "save_results": false
}
```

#### Image-to-Image Search
```bash
POST /search/image
Content-Type: multipart/form-data

form-data:
  - image: <file>
  - k: 10
  - metadata_filter: {"category": "flower"}
  - save_results: false
```

#### Collection Info
```bash
GET /collections/info
```
Returns collection statistics (count, vector size, distance metric).

#### Available Categories
```bash
GET /metadata/categories
```
Returns list of all categories in the collection.

#### Get Saved Results
```bash
GET /results/{result_id}
```
Retrieves previously saved search results.

See full API documentation at http://localhost:8000/docs when running.

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Qdrant**: Vector database for similarity search
- **CLIP (ViT-B-32)**: Image embeddings (512 dimensions)
- **OpenAI GPT-4o-mini**: Query translation and enhancement
- **PyTorch**: Deep learning framework
- **Uvicorn**: ASGI server

### Frontend
- **React Native**: Cross-platform mobile framework
- **Expo**: Development toolchain
- **React Navigation**: Tab navigation
- **react-native-paper**: Material Design components
- **expo-image-picker**: Camera/gallery access
- **axios**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD (in progress)

## 📁 Project Structure

```
SEMANTIC-IMAGE-SEARCH/
├── semantic_image_search/
│   ├── backend/
│   │   ├── api_main.py           # FastAPI application
│   │   └── retriever.py          # Search service
│   ├── config/                   # Configuration files
│   ├── src/
│   │   ├── models/               # CLIP model loaders
│   │   ├── services/             # Business logic
│   │   ├── storage/              # Image storage
│   │   └── vectorstore/          # Qdrant integration
│   └── tests/                    # Test scripts
├── mobile-app/
│   ├── screens/                  # UI screens
│   │   ├── HomeScreen.js
│   │   ├── TextSearchScreen.js
│   │   └── ImageSearchScreen.js
│   ├── components/               # Reusable components
│   ├── services/                 # API client
│   └── App.js                    # Main entry point
├── docker-compose.yml            # Docker orchestration
├── Dockerfile.backend            # Backend container
├── start-docker.sh               # Quick start script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🧪 Testing

### Backend Tests

```bash
# Run API tests
python semantic_image_search/tests/test_api.py

# Quick demo
python semantic_image_search/tests/quick_demo.py

# Metadata filtering demo
python semantic_image_search/tests/metadata_filtering_demo.py
```

### Frontend Testing

```bash
cd mobile-app
npm test  # Run Jest tests (if configured)
```

## 🔧 Configuration

### Backend Configuration

Edit `.env` or environment variables:

```bash
# Required
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=semantic_images

# Optional
LOG_LEVEL=INFO
BACKEND_PORT=8000
```

### Frontend Configuration

Edit `mobile-app/services/api.js`:

```javascript
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';
```

Set environment variable for Expo:
```bash
export EXPO_PUBLIC_API_URL=http://your-backend-url:8000
```

## 🐛 Troubleshooting

### Backend Issues

**NumPy Compatibility Error**:
```bash
# Ensure NumPy < 2.0 for PyTorch compatibility
pip install "numpy<2"
```

**Cannot Connect to Qdrant**:
- Verify QDRANT_URL and QDRANT_API_KEY in .env
- Check network connectivity
- Ensure collection exists

**Metadata Filter Errors**:
- Metadata filter must be valid JSON string
- Example: `{"category": "flower"}`, not just `"flower"`
- See API docs for examples

### Frontend Issues

**Cannot Connect to Backend**:
- Verify backend is running: `curl http://localhost:8000/health`
- Check API_BASE_URL in services/api.js
- For physical devices, use computer's IP, not localhost

**Expo Not Starting**:
```bash
# Clear cache
expo start -c

# Reinstall dependencies
rm -rf node_modules && npm install
```

**Permission Denied (Camera/Photos)**:
- Grant permissions in device settings
- iOS: Settings → Privacy → Camera/Photos
- Android: Settings → Apps → Permissions

See [DOCKER_SETUP.md](DOCKER_SETUP.md) and [mobile-app/README.md](mobile-app/README.md) for more troubleshooting tips.

## 📈 Performance

- **Search Speed**: < 100ms for text queries (after model loading)
- **Image Processing**: ~200-500ms for image encoding
- **Vector Search**: < 50ms with Qdrant (depending on collection size)
- **Concurrent Requests**: Supports multiple simultaneous searches

## 🔒 Security

- CORS enabled for cross-origin requests
- API key authentication via environment variables
- Input validation on all endpoints
- File upload size limits
- Temporary file cleanup

## 🚧 Roadmap

- [ ] User authentication and authorization
- [ ] Image thumbnail display in mobile app
- [ ] Saved results management screen
- [ ] Advanced filtering (multi-category, date ranges)
- [ ] Search history and favorites
- [ ] Batch image upload and indexing
- [ ] Analytics dashboard
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Kubernetes deployment configuration
- [ ] Performance monitoring with Prometheus/Grafana

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for CLIP and GPT models
- [Qdrant](https://qdrant.tech/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [Expo](https://expo.dev/) for React Native development tools

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in `DOCKER_SETUP.md` and `mobile-app/README.md`
- Review API docs at http://localhost:8000/docs

---

**Happy Searching!** 🔍✨
