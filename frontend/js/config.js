/**
 * Configuration
 * 
 * Centralized configuration for the frontend application.
 * 
 * Educational Note:
 * Keeping configuration separate makes it easy to change settings
 * for different environments (development, staging, production).
 */

const CONFIG = {
    // API Configuration
    API_BASE_URL: 'http://localhost:8000',
    API_V1_PREFIX: '/api/v1',
    
    // Game Settings
    COMMAND_HISTORY_SIZE: 50,
    AUTO_SCROLL: true,
    
    // UI Settings
    TYPING_SPEED: 0, // Set to 0 for instant, or ms per character for typing effect
    
    // Get full API URL
    getApiUrl: function(endpoint) {
        return `${this.API_BASE_URL}${this.API_V1_PREFIX}${endpoint}`;
    }
};

// Make CONFIG available globally
window.CONFIG = CONFIG;
