// API Configuration
const API_ENDPOINT = 'https://ytxzaqj65a.execute-api.us-east-1.amazonaws.com';

// DOM Elements
const poemForm = document.getElementById('poemForm');
const topicInput = document.getElementById('topic');
const generateBtn = document.getElementById('generateBtn');
const poemDisplay = document.getElementById('poemDisplay');
const poemTitle = document.getElementById('poemTitle');
const poemContent = document.getElementById('poemContent');
const errorDisplay = document.getElementById('errorDisplay');
const errorMessage = document.getElementById('errorMessage');
const copyBtn = document.getElementById('copyBtn');
const newPoemBtn = document.getElementById('newPoemBtn');
const tryAgainBtn = document.getElementById('tryAgainBtn');

// Event Listeners
poemForm.addEventListener('submit', handleSubmit);
copyBtn.addEventListener('click', copyPoem);
newPoemBtn.addEventListener('click', resetForm);
tryAgainBtn.addEventListener('click', resetForm);

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    const topic = topicInput.value.trim();
    if (!topic) return;
    
    // Show loading state
    generateBtn.classList.add('loading');
    hideElements([poemDisplay, errorDisplay]);
    
    try {
        // Make API call
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic }),
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayPoem(topic, data.poem);
        } else {
            throw new Error(data.error || 'Failed to generate poem');
        }
    } catch (error) {
        displayError(error.message);
    } finally {
        generateBtn.classList.remove('loading');
    }
}

// Display the generated poem
function displayPoem(topic, poem) {
    poemTitle.textContent = `A Poem About ${topic}`;
    poemContent.textContent = poem;
    
    showElement(poemDisplay);
    poemDisplay.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display error message
function displayError(message) {
    errorMessage.textContent = message;
    showElement(errorDisplay);
}

// Copy poem to clipboard
async function copyPoem() {
    const poemText = `${poemTitle.textContent}\n\n${poemContent.textContent}`;
    
    try {
        await navigator.clipboard.writeText(poemText);
        
        // Show success feedback
        copyBtn.classList.add('copied');
        copyBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        `;
        
        // Reset after 2 seconds
        setTimeout(() => {
            copyBtn.classList.remove('copied');
            copyBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
            `;
        }, 2000);
    } catch (err) {
        console.error('Failed to copy:', err);
    }
}

// Reset form and UI
function resetForm() {
    topicInput.value = '';
    topicInput.focus();
    hideElements([poemDisplay, errorDisplay]);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Utility functions
function showElement(element) {
    element.classList.remove('hidden');
}

function hideElements(elements) {
    elements.forEach(el => el.classList.add('hidden'));
}

// Add some example topics on page load
const exampleTopics = [
    'sunset over the ocean',
    'first day of spring',
    'childhood memories',
    'city lights at night',
    'morning coffee',
    'rainy days',
    'starry night sky',
    'autumn leaves'
];

// Set a random placeholder on page load
window.addEventListener('load', () => {
    const randomTopic = exampleTopics[Math.floor(Math.random() * exampleTopics.length)];
    topicInput.placeholder = `e.g., ${randomTopic}...`;
    topicInput.focus();
});

// Add enter key support for new poem button
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !poemDisplay.classList.contains('hidden')) {
        if (document.activeElement !== topicInput) {
            resetForm();
        }
    }
}); 