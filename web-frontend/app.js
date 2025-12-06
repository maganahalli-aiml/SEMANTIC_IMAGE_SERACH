// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State
let currentTab = 'text';
let uploadedImage = null;
let categories = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing application...');
    
    try {
        initializeTabs();
        initializeTextSearch();
        initializeImageSearch();
        loadCategories();
        loadCollectionInfo();
        console.log('Application initialized successfully');
    } catch (error) {
        console.error('Initialization error:', error);
        alert('Failed to initialize application: ' + error.message);
    }
});

// Tab Management
function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            
            // Update active states
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(`${tabName}-search`).classList.add('active');
            
            currentTab = tabName;
        });
    });
}

// Text Search
function initializeTextSearch() {
    console.log('initializeTextSearch called');
    
    const searchBtn = document.getElementById('text-search-btn');
    const queryInput = document.getElementById('text-query');
    
    console.log('Search button:', searchBtn);
    console.log('Query input:', queryInput);

    if (!searchBtn) {
        console.error('Search button not found! ID: text-search-btn');
        return;
    }
    
    if (!queryInput) {
        console.error('Query input not found! ID: text-query');
        return;
    }

    console.log('Attaching click event to search button');
    searchBtn.addEventListener('click', (e) => {
        console.log('Search button clicked!');
        e.preventDefault();
        handleTextSearch();
    });
    
    console.log('Attaching keypress event to query input');
    queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            console.log('Enter key pressed');
            e.preventDefault();
            handleTextSearch();
        }
    });
    
    console.log('Text search initialized successfully');
}

async function handleTextSearch() {
    console.log('handleTextSearch called');
    
    const queryInput = document.getElementById('text-query');
    const categorySelect = document.getElementById('text-category');
    const kInput = document.getElementById('text-k');
    
    if (!queryInput || !categorySelect || !kInput) {
        console.error('Form elements not found!');
        alert('Error: Form elements not found. Please refresh the page.');
        return;
    }
    
    const query = queryInput.value.trim();
    const category = categorySelect.value;
    const k = parseInt(kInput.value);

    console.log('Search params:', { query, category, k });

    if (!query) {
        console.warn('Empty search query');
        return;
    }

    const payload = {
        query_text: query,
        k: k,
        save_results: false
    };

    if (category) {
        payload.metadata_filter = { category: category };
    }

    console.log('Sending request to:', `${API_BASE_URL}/search/text`);
    console.log('Payload:', payload);

    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/search/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Response data:', data);
        displayResults(data, query);
    } catch (error) {
        console.error('Search error:', error);
        console.error('Search failed:', error.message);
    } finally {
        showLoading(false);
    }
}

// Image Search
function initializeImageSearch() {
    const uploadInput = document.getElementById('image-upload');
    const searchBtn = document.getElementById('image-search-btn');
    const clearBtn = document.getElementById('clear-image');
    const uploadLabel = document.querySelector('.upload-label');

    uploadInput.addEventListener('change', handleImageUpload);
    searchBtn.addEventListener('click', handleImageSearch);
    clearBtn.addEventListener('click', clearImage);

    // Drag and drop
    uploadLabel.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadLabel.style.borderColor = '#667eea';
        uploadLabel.style.background = '#f8f9ff';
    });

    uploadLabel.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadLabel.style.borderColor = '#ccc';
        uploadLabel.style.background = 'transparent';
    });

    uploadLabel.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadLabel.style.borderColor = '#ccc';
        uploadLabel.style.background = 'transparent';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageFile(files[0]);
        }
    });
}

function handleImageUpload(e) {
    const file = e.target.files[0];
    if (file) {
        handleImageFile(file);
    }
}

function handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
        console.warn('Invalid file type');
        return;
    }

    uploadedImage = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImg = document.getElementById('preview-image');
        const previewContainer = document.getElementById('preview-container');
        
        previewImg.src = e.target.result;
        previewContainer.classList.remove('hidden');
        document.querySelector('.upload-label').style.display = 'none';
        document.getElementById('image-search-btn').disabled = false;
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    uploadedImage = null;
    document.getElementById('image-upload').value = '';
    document.getElementById('preview-container').classList.add('hidden');
    document.querySelector('.upload-label').style.display = 'block';
    document.getElementById('image-search-btn').disabled = true;
}

async function handleImageSearch() {
    if (!uploadedImage) {
        console.warn('No image uploaded');
        return;
    }

    const category = document.getElementById('image-category').value;
    const k = parseInt(document.getElementById('image-k').value);

    const formData = new FormData();
    formData.append('image', uploadedImage);
    formData.append('k', k);
    formData.append('save_results', 'false');
    
    if (category) {
        // Send metadata_filter as JSON string
        const metadataFilter = JSON.stringify({ category: category });
        formData.append('metadata_filter', metadataFilter);
    }

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/search/image`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data, 'Image Search');
    } catch (error) {
        console.error('Search error:', error);
        console.error('Image search failed:', error);
    } finally {
        showLoading(false);
    }
}

// Display Results
function displayResults(data, query) {
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const resultsInfo = document.getElementById('results-info');

    resultsSection.classList.remove('hidden');
    resultsGrid.innerHTML = '';

    resultsInfo.textContent = `Found ${data.total_results} results for "${query}"`;

    if (data.total_results === 0) {
        resultsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #999; padding: 40px;">No results found. Try a different query or remove filters.</p>';
        return;
    }

    data.results.forEach(result => {
        const card = createResultCard(result);
        resultsGrid.appendChild(card);
    });

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function createResultCard(result) {
    const card = document.createElement('div');
    card.className = 'result-card';

    const score = (result.score * 100).toFixed(1);
    
    // Fetch image from backend using the image ID
    const imageSrc = `${API_BASE_URL}/images/${result.id}`;

    card.innerHTML = `
        <img src="${imageSrc}" alt="${result.payload.filename}" class="result-image">
        <div class="result-info">
            <div class="result-filename" title="${result.payload.filename}">${result.payload.filename}</div>
            <div class="result-meta">
                <span class="result-category">${result.payload.category || 'uncategorized'}</span>
                <span class="result-score">${score}%</span>
            </div>
        </div>
    `;

    // Add error handler to image element
    const img = card.querySelector('.result-image');
    img.onerror = function() {
        this.style.display = 'none';
        const placeholder = document.createElement('div');
        placeholder.className = 'result-image';
        placeholder.style.cssText = 'background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px;';
        placeholder.textContent = result.payload.filename;
        this.parentNode.replaceChild(placeholder, this);
    };

    card.addEventListener('click', () => {
        console.log('Image clicked:', result.payload);
    });

    return card;
}

// Load Categories
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/metadata/categories`);
        const data = await response.json();
        
        categories = data.categories || [];
        
        const textSelect = document.getElementById('text-category');
        const imageSelect = document.getElementById('image-category');
        
        categories.forEach(category => {
            const option1 = document.createElement('option');
            option1.value = category;
            option1.textContent = category.charAt(0).toUpperCase() + category.slice(1);
            textSelect.appendChild(option1);
            
            const option2 = document.createElement('option');
            option2.value = category;
            option2.textContent = category.charAt(0).toUpperCase() + category.slice(1);
            imageSelect.appendChild(option2);
        });
    } catch (error) {
        console.error('Failed to load categories:', error);
    }
}

// Load Collection Info
async function loadCollectionInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/collections/info`);
        const data = await response.json();
        
        const statusDiv = document.getElementById('collection-status');
        statusDiv.innerHTML = `
            <div class="status-item">
                <div class="status-label">Collection Name</div>
                <div class="status-value" style="font-size: 1rem;">${data.collection_name}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Total Images</div>
                <div class="status-value">${data.points_count}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Vector Size</div>
                <div class="status-value">${data.config.vector_size}</div>
            </div>
            <div class="status-item">
                <div class="status-label">Status</div>
                <div class="status-value" style="color: ${data.status === 'GREEN' ? '#4CAF50' : '#ff9800'};">${data.status}</div>
            </div>
        `;
    } catch (error) {
        console.error('Failed to load collection info:', error);
        document.getElementById('collection-status').innerHTML = '<p style="color: #ff4444;">Failed to connect to backend</p>';
    }
}

// Loading State
function showLoading(show) {
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('results-section');
    
    if (show) {
        loading.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    } else {
        loading.classList.add('hidden');
    }
}
