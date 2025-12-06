# Semantic Image Search - Mobile App

A React Native mobile application for semantic image search, powered by CLIP embeddings and Qdrant vector database. Search for similar images using text descriptions or by uploading photos directly from your device.

## Features

- 🔍 **Text-to-Image Search**: Find images using natural language descriptions
- 📷 **Image-to-Image Search**: Upload photos from gallery or camera to find similar images
- 🏷️ **Category Filtering**: Filter search results by categories (flowers, animals, nature, etc.)
- 📊 **Dashboard**: View backend health status and collection information
- 🎨 **Material Design**: Beautiful UI built with react-native-paper components

## Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (v16 or higher)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)
- [Expo CLI](https://docs.expo.dev/get-started/installation/) (`npm install -g expo-cli`)
- iOS Simulator (Mac only) or Android Emulator
- [Expo Go app](https://expo.dev/client) on your physical device (optional)

## Backend Requirements

This mobile app requires the Semantic Image Search backend to be running. Make sure you have:

1. Backend API running on `http://localhost:8000` (or your specified URL)
2. Qdrant vector database connected with indexed images
3. CLIP model loaded for embeddings

See the main project README for backend setup instructions.

## Installation

1. Navigate to the mobile app directory:
   ```bash
   cd mobile-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```
   or with yarn:
   ```bash
   yarn install
   ```

## Configuration

### Backend API URL

Update the API base URL in `services/api.js` based on your testing environment:

**For iOS Simulator (Mac):**
```javascript
const API_BASE_URL = 'http://localhost:8000';  // or your Mac's IP
```

**For Android Emulator:**
```javascript
const API_BASE_URL = 'http://10.0.2.2:8000';  // Android emulator special IP
```

**For Physical Device (Expo Go):**
```javascript
const API_BASE_URL = 'http://192.168.1.X:8000';  // Replace with your computer's local IP
```

To find your computer's local IP:
- **Mac**: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- **Linux**: `ip addr show | grep "inet " | grep -v 127.0.0.1`
- **Windows**: `ipconfig` (look for IPv4 Address)

**Important**: Make sure your device and computer are on the same Wi-Fi network when testing on physical devices.

## Running the App

1. Start the Expo development server:
   ```bash
   npm start
   ```
   or with yarn:
   ```bash
   yarn start
   ```
   or directly with Expo:
   ```bash
   expo start
   ```

2. Choose your testing platform:
   - Press `i` for iOS simulator (Mac only)
   - Press `a` for Android emulator
   - Scan the QR code with Expo Go app on your physical device

## App Structure

```
mobile-app/
├── App.js                      # Main entry point with navigation
├── app.json                    # Expo configuration
├── package.json                # Dependencies and scripts
├── babel.config.js            # Babel configuration
├── assets/                    # App icons and splash screen
├── components/                # Reusable components
│   └── SearchResults.js       # Display search results
├── screens/                   # Main app screens
│   ├── HomeScreen.js         # Dashboard with backend status
│   ├── TextSearchScreen.js   # Text-to-image search
│   └── ImageSearchScreen.js  # Image-to-image search
└── services/                  # API integration
    └── api.js                 # Backend API client
```

## Usage

### Home Screen
- View backend health status and connection info
- See collection statistics (number of indexed images, vector dimensions)
- Quick guide to app features

### Text Search
1. Enter a text description (e.g., "red flowers", "animals in nature")
2. (Optional) Filter by category using the filter button
3. Tap "Search" to find matching images
4. View results with similarity scores and metadata

### Image Search
1. Choose "Choose Photo" to pick from gallery or "Take Photo" to use camera
2. Grant camera/photo library permissions when prompted
3. (Optional) Apply category filter
4. Tap "Search" to find similar images
5. View results ranked by similarity

## Troubleshooting

### Cannot Connect to Backend

**Error**: "Failed to connect to backend" or "Network Error"

**Solutions**:
1. Verify backend is running:
   ```bash
   cd /path/to/backend
   ./run_api.sh
   ```
   Check that you see "Application startup complete" and server is on port 8000

2. Check API_BASE_URL in `services/api.js`:
   - For physical device, use your computer's local IP, not `localhost`
   - Ensure device and computer are on the same Wi-Fi network
   - Verify firewall isn't blocking port 8000

3. Test backend directly:
   ```bash
   curl http://localhost:8000/health
   # or with your IP
   curl http://192.168.1.X:8000/health
   ```

### Camera/Photo Library Permissions

**Error**: "Permission denied" when trying to access camera or photos

**Solutions**:
1. Grant permissions when prompted on first use
2. Check device settings:
   - **iOS**: Settings → Privacy → Camera/Photos → Semantic Image Search → Enable
   - **Android**: Settings → Apps → Semantic Image Search → Permissions → Enable Camera/Storage

3. On iOS simulator, you may need to manually select photos since camera hardware isn't available

### No Search Results

**Issue**: Search returns empty results

**Possible Causes**:
1. No images indexed in backend - check backend logs and collection info on Home screen
2. Query too specific - try broader search terms
3. Category filter too restrictive - try removing filters
4. Backend model not loaded - check backend logs for CLIP model loading errors

### App Won't Start

**Error**: Metro bundler fails or app crashes on startup

**Solutions**:
1. Clear Expo cache:
   ```bash
   expo start -c
   ```

2. Delete node_modules and reinstall:
   ```bash
   rm -rf node_modules
   npm install
   ```

3. Check Node.js version (should be v16+):
   ```bash
   node --version
   ```

## Development

### Adding New Dependencies

```bash
npm install <package-name>
# or
yarn add <package-name>
```

### Running on Specific Platform

```bash
# iOS only
npm run ios

# Android only
npm run android

# Web (experimental)
npm run web
```

### Debugging

1. Open React Native debugger: Shake device (physical) or press `Cmd+D` (iOS) / `Cmd+M` (Android)
2. Select "Debug Remote JS" or "Open React DevTools"
3. View console logs in terminal where `expo start` is running

## Building for Production

### Using Expo Application Services (EAS)

1. Install EAS CLI:
   ```bash
   npm install -g eas-cli
   ```

2. Login to Expo:
   ```bash
   eas login
   ```

3. Configure build:
   ```bash
   eas build:configure
   ```

4. Build for iOS/Android:
   ```bash
   eas build --platform ios
   eas build --platform android
   eas build --platform all
   ```

5. Submit to stores:
   ```bash
   eas submit --platform ios
   eas submit --platform android
   ```

### Update API URL for Production

Before building, update `services/api.js` with your production backend URL:
```javascript
const API_BASE_URL = 'https://your-production-api.com';  // Replace with actual URL
```

## Technologies Used

- **React Native**: Cross-platform mobile framework
- **Expo**: Development toolchain and SDK
- **React Navigation**: Tab-based navigation
- **react-native-paper**: Material Design components
- **expo-image-picker**: Camera and photo library access
- **axios**: HTTP client for API requests

## API Endpoints Used

- `GET /health` - Backend health check
- `GET /collections/info` - Collection statistics
- `GET /metadata/categories` - Available categories
- `POST /search/text` - Text-to-image search
- `POST /search/image` - Image-to-image search
- `GET /results/{id}` - Retrieve saved results

See the main API documentation for detailed endpoint specifications.

## Known Limitations

1. **Image Display**: Currently showing metadata only; actual image thumbnails require additional backend endpoint
2. **Saved Results**: UI for viewing saved search results not yet implemented
3. **Offline Mode**: No offline support; requires active backend connection
4. **File Size**: Large images (>5MB) may take longer to upload

## Future Enhancements

- [ ] Display image thumbnails in search results
- [ ] Saved search results management screen
- [ ] Advanced filtering (multiple categories, year, verified status)
- [ ] Search history and favorites
- [ ] Offline caching of recent results
- [ ] Image zoom and detailed view
- [ ] Share search results
- [ ] Dark mode support

## Contributing

1. Make changes in a feature branch
2. Test on both iOS and Android
3. Update this README if adding new features
4. Submit pull request

## Support

For issues related to:
- **Backend API**: See main project documentation
- **Mobile App**: Open an issue in the project repository
- **Expo**: Check [Expo documentation](https://docs.expo.dev/)

## License

This project is part of the Semantic Image Search system. See main project LICENSE file.
