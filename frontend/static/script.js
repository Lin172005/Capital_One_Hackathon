// DOM Elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const loadingOverlay = document.getElementById('loading-overlay');
const statusIndicator = document.getElementById('status-indicator');
const statusIcon = document.getElementById('status-icon');
const statusText = document.getElementById('status-text');

// Connectivity state
let isOnline = false;
let currentModel = '';

// Tab switching functionality
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        
        // Remove active class from all tabs and contents
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding content
        btn.classList.add('active');
        document.getElementById(`${targetTab}-tab`).classList.add('active');
    });
});

// Utility functions
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

function showResponse(elementId, response, isError = false) {
    const responseElement = document.getElementById(elementId);
    const answerElement = responseElement.querySelector('.response-content');
    
    responseElement.classList.remove('hidden');
    responseElement.classList.remove('success', 'error');
    
    if (isError) {
        responseElement.classList.add('error');
        answerElement.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle"></i> ${response}</div>`;
    } else {
        responseElement.classList.add('success');
        answerElement.innerHTML = response;
    }
}

function hideResponse(elementId) {
    const responseElement = document.getElementById(elementId);
    responseElement.classList.add('hidden');
}

// Connectivity detection
async function checkConnectivity() {
    try {
        // Try to fetch a small resource to test connectivity
        const response = await fetch('https://www.google.com/favicon.ico', { 
            method: 'HEAD',
            mode: 'no-cors',
            cache: 'no-cache'
        });
        return true;
    } catch (error) {
        return false;
    }
}

// Update status indicator
function updateStatusIndicator(online, model = '') {
    isOnline = online;
    currentModel = model;
    
    statusIndicator.className = 'status-indicator';
    
    if (online) {
        statusIndicator.classList.add('online');
        statusIcon.className = 'fas fa-circle';
        statusText.textContent = `Online - Using ${model}`;
    } else {
        statusIndicator.classList.add('offline');
        statusIcon.className = 'fas fa-circle';
        statusText.textContent = `Offline - Using ${model}`;
    }
}

// Initialize connectivity check
async function initializeConnectivity() {
    statusIndicator.classList.add('checking');
    statusText.textContent = 'Checking connectivity...';
    
    const online = await checkConnectivity();
    
    if (online) {
        updateStatusIndicator(true, 'Gemini AI');
    } else {
        updateStatusIndicator(false, 'Phi-3 (Local)');
    }
}

// Unified Query Handler
document.getElementById('submit-query').addEventListener('click', async () => {
    const query = document.getElementById('main-query').value.trim();
    
    if (!query) {
        alert('Please enter a question');
        return;
    }
    
    showLoading();
    hideResponse('query-response');
    
    try {
        // Determine which endpoint to use based on connectivity
        let endpoint, modelName;
        
        if (isOnline) {
            endpoint = '/api/text-query';
            modelName = 'Gemini AI';
        } else {
            endpoint = '/api/offline-query';
            modelName = 'Phi-3 (Local)';
        }
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: query })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Update the response source to show which model was used
            const responseSource = document.querySelector('#query-response .response-source');
            responseSource.textContent = `AI Response (${modelName})`;
            
            showResponse('query-response', data.answer);
        } else {
            showResponse('query-response', data.answer || 'An error occurred', true);
        }
    } catch (error) {
        console.error('Error:', error);
        
        // If online query fails, try offline as fallback
        if (isOnline) {
            try {
                console.log('Online query failed, trying offline fallback...');
                const fallbackResponse = await fetch('/api/offline-query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: query })
                });
                
                const fallbackData = await fallbackResponse.json();
                
                if (fallbackResponse.ok) {
                    const responseSource = document.querySelector('#query-response .response-source');
                    responseSource.textContent = `AI Response (Phi-3 Local - Fallback)`;
                    showResponse('query-response', fallbackData.answer);
                    return;
                }
            } catch (fallbackError) {
                console.error('Fallback also failed:', fallbackError);
            }
        }
        
        showResponse('query-response', 'Network error. Please try again.', true);
    } finally {
        hideLoading();
    }
});

// Image Upload and Analysis
const uploadArea = document.getElementById('upload-area');
const imageInput = document.getElementById('image-input');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const removeImageBtn = document.getElementById('remove-image');
const submitImageBtn = document.getElementById('submit-image');

let selectedFile = null;

// Handle file selection
uploadArea.addEventListener('click', () => {
    imageInput.click();
});

// Handle drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#45a049';
    uploadArea.style.background = 'rgba(76, 175, 80, 0.1)';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#4CAF50';
    uploadArea.style.background = 'rgba(76, 175, 80, 0.05)';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#4CAF50';
    uploadArea.style.background = 'rgba(76, 175, 80, 0.05)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// Handle file input change
imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Handle file selection
function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        uploadArea.classList.add('hidden');
        imagePreview.classList.remove('hidden');
        submitImageBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

// Remove image
removeImageBtn.addEventListener('click', () => {
    selectedFile = null;
    imageInput.value = '';
    imagePreview.classList.add('hidden');
    uploadArea.classList.remove('hidden');
    submitImageBtn.disabled = true;
    hideResponse('image-response');
});

// Submit image for analysis
submitImageBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        alert('Please select an image first');
        return;
    }
    
    showLoading();
    hideResponse('image-response');
    
    try {
        const formData = new FormData();
        formData.append('image', selectedFile);
        
        const response = await fetch('/api/image-diagnosis', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResponse('image-response', data.answer);
        } else {
            showResponse('image-response', data.answer || 'An error occurred during image analysis', true);
        }
    } catch (error) {
        console.error('Error:', error);
        showResponse('image-response', 'Network error. Please try again.', true);
    } finally {
        hideLoading();
    }
});

// Enter key support for text areas
document.getElementById('main-query').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        document.getElementById('submit-query').click();
    }
});

// Auto-resize textareas
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

document.getElementById('main-query').addEventListener('input', function() {
    autoResize(this);
});

// Add some visual feedback for better UX
document.querySelectorAll('.submit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        // Add a small click effect
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
});

// Initialize the first tab as active
document.addEventListener('DOMContentLoaded', () => {
    // Ensure the first tab is active by default
    const firstTab = document.querySelector('.tab-btn[data-tab="query"]');
    const firstContent = document.getElementById('query-tab');
    
    if (firstTab && firstContent) {
        firstTab.classList.add('active');
        firstContent.classList.add('active');
    }
    
    // Initialize connectivity check
    initializeConnectivity();
    
    // Add some initial styling
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Network status event listeners
window.addEventListener('online', async () => {
    console.log('Network connection restored');
    await initializeConnectivity();
});

window.addEventListener('offline', async () => {
    console.log('Network connection lost');
    updateStatusIndicator(false, 'Phi-3 (Local)');
});

// Periodic connectivity check (every 30 seconds)
setInterval(async () => {
    if (navigator.onLine) {
        const online = await checkConnectivity();
        if (online !== isOnline) {
            await initializeConnectivity();
        }
    }
}, 30000);

// Add some helpful tooltips or hints
function addHelpfulHints() {
    const hints = [
        'Tip: You can use Ctrl+Enter to submit text queries quickly',
        'Tip: For image diagnosis, make sure the image is clear and well-lit',
        'Tip: The system automatically chooses the best AI model based on connectivity',
        'Tip: Check the bottom-right indicator to see which AI model is being used'
    ];
    
    // You could implement a rotating hint system here
    console.log('Helpful hints available:', hints);
}

// Initialize helpful hints
addHelpfulHints();
