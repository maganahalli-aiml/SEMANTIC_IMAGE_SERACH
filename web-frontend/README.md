# Web Frontend - Semantic Image Search

A modern, responsive web interface for the Semantic Image Search application.

## Features

- 🔍 **Text Search**: Search images using natural language queries
- 🖼️ **Image Search**: Upload an image to find similar images
- 🏷️ **Category Filtering**: Filter results by category
- 📊 **Collection Status**: View real-time collection statistics
- 🎨 **Modern UI**: Clean, gradient-based design with smooth animations
- 📱 **Responsive**: Works on desktop, tablet, and mobile devices

## Quick Start

### Using Docker (Recommended)

```bash
# Start the web frontend along with backend
docker-compose up -d

# Access the application
open http://localhost:3000
```

### Local Development

```bash
# Navigate to web frontend directory
cd web-frontend

# Serve with any static file server
python3 -m http.server 3000

# Or use Node.js
npx serve -p 3000

# Access at http://localhost:3000
```

## Usage

### Text Search
1. Click on the "Text Search" tab (default)
2. Enter a natural language query (e.g., "yellow flowers", "wild animals")
3. Optionally select a category filter
4. Adjust the number of results (default: 10)
5. Click "Search"

### Image Search
1. Click on the "Image Search" tab
2. Upload an image by clicking or dragging and dropping
3. Optionally select a category filter
4. Adjust the number of results
5. Click "Search Similar"

### View Results
- Results are displayed in a grid layout
- Each card shows:
  - Image filename
  - Category tag
  - Similarity score (%)
- Click on any result card to see more details

## API Integration

The frontend connects to the backend API at `http://localhost:8000` by default.

To change the API URL, edit `app.js`:

```javascript
const API_BASE_URL = 'http://your-backend-url:port';
```

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients, animations, and grid layouts
- **Vanilla JavaScript**: No frameworks, pure JS for maximum performance
- **Nginx**: Web server for production deployment

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Customization

### Colors
Edit `styles.css` to change the color scheme:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Layout
Adjust grid columns in `styles.css`:

```css
.results-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}
```

## Development

The frontend is static HTML/CSS/JS with no build step required. Simply edit the files and refresh your browser.

### File Structure
```
web-frontend/
├── index.html      # Main HTML structure
├── styles.css      # All styling
├── app.js          # Application logic
├── nginx.conf      # Nginx configuration
└── Dockerfile      # Docker container definition
```

## Troubleshooting

### Backend Connection Failed
- Ensure the backend is running: `curl http://localhost:8000/health`
- Check CORS is enabled in the backend
- Verify the API_BASE_URL in `app.js`

### No Results Found
- Verify images are indexed in the collection
- Check category filters match your data
- Try searching without filters first

### Image Upload Not Working
- Ensure the backend accepts the `/search/image` endpoint
- Check file size limits (< 10MB recommended)
- Verify supported formats: JPG, PNG, WEBP

## License

Part of the Semantic Image Search project.
