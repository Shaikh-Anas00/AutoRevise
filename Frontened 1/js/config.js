/**
 * Frontend Configuration
 * This file contains configuration settings for the frontend application
 * Update API_BASE_URL to match your backend server location
 */

const CONFIG = {
    // API Base URL - Change this if your backend is hosted elsewhere
    API_BASE_URL: 'http://127.0.0.1:5000',
    
    // Alternative: Use environment-based configuration
    // For production, you would replace this with your production API URL
    // API_BASE_URL: window.location.hostname === 'localhost' 
    //     ? 'http://127.0.0.1:5000' 
    //     : 'https://your-production-api.com'
};

// Make CONFIG available globally
window.CONFIG = CONFIG;
