import axios from 'axios';

// Update this to your backend URL
// For local development on iOS simulator: use your computer's IP address
// For Android emulator: use 10.0.2.2
// For physical device: use your computer's IP address on the same network
// For Docker: use 'http://backend:8000' (internal) or 'http://localhost:8000' (from host)
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

// Uncomment and update for physical device testing:
// const API_BASE_URL = 'http://YOUR_COMPUTER_IP:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Health check endpoint
 */
export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

/**
 * Get collection info
 */
export const getCollectionInfo = async () => {
  const response = await api.get('/collections/info');
  return response.data;
};

/**
 * Get available metadata categories
 */
export const getCategories = async () => {
  const response = await api.get('/metadata/categories');
  return response.data;
};

/**
 * Text-to-image search
 * @param {string} queryText - Search query text
 * @param {number} k - Number of results (default: 10)
 * @param {object} metadataFilter - Optional metadata filter (e.g., {category: "flower"})
 * @param {boolean} saveResults - Whether to save results (default: false)
 */
export const searchByText = async (queryText, k = 10, metadataFilter = null, saveResults = false) => {
  const response = await api.post('/search/text', {
    query_text: queryText,
    k,
    metadata_filter: metadataFilter,
    save_results: saveResults,
  });
  return response.data;
};

/**
 * Image-to-image search
 * @param {string} imageUri - Local image URI
 * @param {number} k - Number of results (default: 10)
 * @param {object} metadataFilter - Optional metadata filter
 * @param {boolean} saveResults - Whether to save results (default: false)
 */
export const searchByImage = async (imageUri, k = 10, metadataFilter = null, saveResults = false) => {
  const formData = new FormData();
  
  // Extract filename from URI
  const filename = imageUri.split('/').pop();
  const match = /\.(\w+)$/.exec(filename);
  const type = match ? `image/${match[1]}` : 'image/jpeg';

  formData.append('image', {
    uri: imageUri,
    name: filename,
    type: type,
  });

  formData.append('k', k);
  formData.append('save_results', saveResults);
  
  if (metadataFilter) {
    formData.append('metadata_filter', JSON.stringify(metadataFilter));
  }

  const response = await api.post('/search/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Get saved results by ID
 * @param {string} resultId - Result UUID
 */
export const getSavedResults = async (resultId) => {
  const response = await api.get(`/results/${resultId}`);
  return response.data;
};

/**
 * Build image URL from result payload
 * @param {object} result - Search result object with payload
 */
export const getImageUrl = (result) => {
  if (result.payload && result.payload.path) {
    // For local development, you might need to serve images separately
    // or modify this to match your setup
    return result.payload.path;
  }
  return null;
};

export default api;
