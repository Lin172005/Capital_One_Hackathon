// DOM Elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const loadingOverlay = document.getElementById('loading-overlay');
const statusIndicator = document.getElementById('status-indicator');
const statusIcon = document.getElementById('status-icon');
const statusText = document.getElementById('status-text');
const mainQueryInput = document.getElementById('main-query');
const submitQueryBtn = document.getElementById('submit-query');
const queryResponseArea = document.getElementById('query-response');
const imageResponseArea = document.getElementById('image-response');

// Image Tab Elements
const uploadArea = document.getElementById('upload-area');
const imageInput = document.getElementById('image-input');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const removeImageBtn = document.getElementById('remove-image');
const submitImageBtn = document.getElementById('submit-image');

let isOnline = navigator.onLine;
let selectedFile = null;

// --- Tab switching functionality ---
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(`${targetTab}-tab`).classList.add('active');
    });
});

// --- Utility functions ---
const showLoading = () => loadingOverlay.classList.remove('hidden');
const hideLoading = () => loadingOverlay.classList.add('hidden');

function showResponse(elementId, response, source, isError = false) {
    const responseElement = document.getElementById(elementId);
    const answerElement = responseElement.querySelector('.response-content');
    const sourceElement = responseElement.querySelector('.response-source');
    
    responseElement.classList.remove('hidden', 'success', 'error');
    
    if (isError) {
        responseElement.classList.add('error');
        answerElement.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle"></i> ${response}</div>`;
        sourceElement.textContent = "Error";
    } else {
        responseElement.classList.add('success');
        answerElement.innerHTML = response.replace(/\n/g, '<br>'); // Format newlines
        sourceElement.textContent = `AI Response (${source})`;
    }
}

// --- Connectivity ---
function updateStatusIndicator() {
    isOnline = navigator.onLine;
    statusIndicator.className = 'status-indicator';
    if (isOnline) {
        statusIndicator.classList.add('online');
        statusIcon.className = 'fas fa-circle';
        statusText.textContent = `Online - Using Gemini AI`;
    } else {
        statusIndicator.classList.add('offline');
        statusIcon.className = 'fas fa-circle';
        statusText.textContent = `Offline - Using Local AI`;
    }
}

// --- Location Handler ---
function getLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                callback({ latitude, longitude });
            },
            () => {
                alert("Could not get your location. Please enable location services. Answering without location data.");
                callback(null); // Proceed without location
            }
        );
    } else {
        callback(null); // Geolocation not supported
    }
}

// --- Text Query Handler ---
submitQueryBtn.addEventListener('click', () => {
    const query = mainQueryInput.value.trim();
    if (!query) {
        alert('Please enter a question');
        return;
    }
    
    const locationKeywords = ['soil', 'market price', 'weather', 'nearby', 'land', 'மண்', 'சந்தை விலை', 'வானிலை'];
    const requiresLocation = locationKeywords.some(keyword => query.toLowerCase().includes(keyword));

    showLoading();
    queryResponseArea.classList.add('hidden');

    if (isOnline && requiresLocation) {
        getLocation(location => {
            fetchTextQuery(query, location);
        });
    } else {
        fetchTextQuery(query, null);
    }
});

async function fetchTextQuery(question, location) {
    const endpoint = isOnline ? '/api/text-query' : '/api/offline-query';
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, location }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.answer || 'An unknown error occurred.');
        }

        showResponse('query-response', data.answer, data.source);

    } catch (error) {
        console.error('Error:', error);
        showResponse('query-response', error.message, 'System Error', true);
    } finally {
        hideLoading();
    }
}

// --- Image Diagnosis Handler ---
submitImageBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    showLoading();
    imageResponseArea.classList.add('hidden');
    
    // This is the key logic: it automatically chooses the right endpoint
    const endpoint = isOnline ? '/api/image-diagnosis' : '/api/offline-image-diagnosis';
    console.log(`Using image diagnosis endpoint: ${endpoint}`);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.answer);
        
        showResponse('image-response', data.answer, data.source);

    } catch (error) {
        showResponse('image-response', error.message, 'System Error', true);
    } finally {
        hideLoading();
    }
});

// --- Image File Selection Logic ---
uploadArea.addEventListener('click', () => imageInput.click());
imageInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));

function handleFileSelect(file) {
    if (!file || !file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        uploadArea.classList.add('hidden');
        imagePreview.classList.remove('hidden');
        submitImageBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

removeImageBtn.addEventListener('click', () => {
    selectedFile = null;
    imageInput.value = '';
    imagePreview.classList.add('hidden');
    uploadArea.classList.remove('hidden');
    submitImageBtn.disabled = true;
    imageResponseArea.classList.add('hidden');
});

// --- Initial Setup ---
window.addEventListener('online', updateStatusIndicator);
window.addEventListener('offline', updateStatusIndicator);
document.addEventListener('DOMContentLoaded', () => {
    updateStatusIndicator();
    const firstTab = document.querySelector('.tab-btn[data-tab="query"]');
    if (firstTab) firstTab.click();
});