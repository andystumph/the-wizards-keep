/**
 * API Module
 * 
 * Handles all communication with the backend API.
 * 
 * Educational Notes:
 * - Fetch API is modern JavaScript for HTTP requests
 * - Async/await makes asynchronous code readable
 * - Error handling is crucial for good UX
 * - Centralized API calls make the codebase maintainable
 */

const API = {
    /**
     * Generic fetch wrapper with error handling
     */
    async request(endpoint, options = {}) {
        const url = CONFIG.getApiUrl(endpoint);
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            
            // Check if response is ok (status 200-299)
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            
            // Parse JSON response
            const data = await response.json();
            return { success: true, data };
            
        } catch (error) {
            console.error('API request failed:', error);
            return {
                success: false,
                error: error.message || 'Network error occurred'
            };
        }
    },

    /**
     * Player API Endpoints
     */
    players: {
        /**
         * Create a new player
         */
        async create(username, characterName) {
            return await API.request('/players/', {
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    character_name: characterName
                })
            });
        },

        /**
         * Get player by ID
         */
        async get(playerId) {
            return await API.request(`/players/${playerId}`);
        },

        /**
         * Get player's game state
         */
        async getGameState(playerId) {
            return await API.request(`/players/${playerId}/game-state`);
        }
    },

    /**
     * Game API Endpoints
     */
    game: {
        /**
         * Send a command to the game engine
         */
        async sendCommand(playerId, command) {
            return await API.request('/game/command', {
                method: 'POST',
                body: JSON.stringify({
                    player_id: playerId,
                    command: command
                })
            });
        },

        /**
         * Reset player's game
         */
        async reset(playerId) {
            return await API.request(`/game/reset/${playerId}`, {
                method: 'POST'
            });
        },

        /**
         * Get help/available commands
         */
        async getHelp() {
            return await API.request('/game/help');
        }
    },

    /**
     * Location API Endpoints
     */
    locations: {
        /**
         * Get location by ID
         */
        async get(locationId) {
            return await API.request(`/locations/${locationId}`);
        }
    },

    /**
     * Item API Endpoints
     */
    items: {
        /**
         * Get player's inventory
         */
        async getInventory(playerId) {
            return await API.request(`/items/player/${playerId}/inventory`);
        }
    },

    /**
     * Health check
     */
    async healthCheck() {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/health`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
};

// Make API available globally
window.API = API;
