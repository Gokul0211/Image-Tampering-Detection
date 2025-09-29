document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const uploadBox = document.getElementById('uploadBox');
    const imageUpload = document.getElementById('imageUpload');
    const previewImage = document.getElementById('previewImage');
    const clearBtn = document.getElementById('clearBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsPlaceholder = document.querySelector('.results-placeholder');
    const resultsContent = document.getElementById('resultsContent');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultStatus = document.getElementById('resultStatus');
    const resultConfidence = document.getElementById('resultConfidence');
    const analysisTime = document.getElementById('analysisTime');
    const elaImageContainer = document.getElementById('elaImageContainer');
    const recommendationText = document.getElementById('recommendationText');

    // Drag and Drop functionality
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.style.background = 'rgba(67, 97, 238, 0.1)';
        uploadBox.style.border = '2px dashed var(--primary)';
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.style.background = '#f8f9fa';
        uploadBox.style.border = 'none';
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.style.background = '#f8f9fa';
        uploadBox.style.border = 'none';
        
        if (e.dataTransfer.files.length) {
            imageUpload.files = e.dataTransfer.files;
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    // File input change handler
    imageUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            handleFileUpload(this.files[0]);
        }
    });

    // Clear button handler
    clearBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        resetUploader();
    });

    // Analyze button handler
    analyzeBtn.addEventListener('click', analyzeImage);

    // Handle file upload
    function handleFileUpload(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            alert('Please upload a valid image file (JPEG, PNG, or WEBP)');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10MB limit');
            return;
        }

        // Display preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            analyzeBtn.disabled = false;
            clearBtn.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    // Reset uploader
    function resetUploader() {
        imageUpload.value = '';
        previewImage.src = '#';
        previewImage.style.display = 'none';
        analyzeBtn.disabled = true;
        clearBtn.style.display = 'none';
        resultsPlaceholder.style.display = 'flex';
        resultsContent.style.display = 'none';
    }

    // Analyze image
    async function analyzeImage() {
        if (!imageUpload.files.length) return;

        // Show loading state
        loadingOverlay.classList.remove('hidden');
        resultsPlaceholder.style.display = 'none';
        resultsContent.style.display = 'none';

        const formData = new FormData();
        formData.append('file', imageUpload.files[0]);
        
        try {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }

            const data = await response.json();
            console.log("API Response:", data); // Debugging log
            
            // Display results using server-provided data
            displayResults(data);

        } catch (error) {
            console.error('Analysis failed:', error);
            loadingOverlay.classList.add('hidden');
            resultsPlaceholder.style.display = 'flex';
            alert('Analysis failed. Please try again or check your connection.');
        }
    }

    // Display analysis results
    function displayResults(data) {
        loadingOverlay.classList.add('hidden');
        resultsPlaceholder.style.display = 'none';
        resultsContent.style.display = 'block';

        // Set status from API response
        const status = data.prediction || 'Unknown';
        resultStatus.textContent = status.charAt(0).toUpperCase() + status.slice(1);

        // Set confidence (convert from decimal to percentage)
        const confidence = data.confidence !== undefined ? (data.confidence * 100) : 0;
        resultConfidence.textContent = `${confidence.toFixed(2)}%`;

        // Use server's processing time (convert seconds to milliseconds if needed)
        const processingTime = data.processing_time !== undefined ? 
            (data.processing_time > 1 ? data.processing_time : data.processing_time * 1000) : 
            0;
        analysisTime.textContent = `${processingTime.toFixed(2)} ms`;

        // Set status color and recommendation
        if (status.toLowerCase() === 'tampered') {
            resultStatus.style.color = 'var(--danger)';
            recommendationText.textContent = 'This image shows signs of digital manipulation. Consider verifying its authenticity through additional means.';
        } else {
            resultStatus.style.color = 'var(--success)';
            recommendationText.textContent = 'No significant signs of tampering detected. The image appears to be authentic.';
        }

        // Display ELA image if available
        if (data.ela_image) {
            elaImageContainer.innerHTML = `<img src="${data.ela_image}" alt="ELA Analysis" class="ela-image">`;
        } else if (data.ela_path) {
            elaImageContainer.innerHTML = `<img src="${data.ela_path}" alt="ELA Analysis" class="ela-image">`;
        } else {
            elaImageContainer.innerHTML = '<p>ELA visualization not available</p>';
        }
    }

    // Sample image click handler for demo purposes
    document.querySelectorAll('.demo-card').forEach(card => {
        card.addEventListener('click', function() {
            const imgPath = this.getAttribute('data-image');
            fetch(imgPath)
                .then(res => res.blob())
                .then(blob => {
                    const file = new File([blob], imgPath.split('/').pop(), { type: blob.type });
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    imageUpload.files = dataTransfer.files;
                    handleFileUpload(file);
                })
                .catch(err => {
                    console.error('Error loading sample image:', err);
                    alert('Failed to load sample image');
                });
        });
    });
});