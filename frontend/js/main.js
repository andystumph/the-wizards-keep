/**
 * Main Entry Point
 * 
 * Initializes the application when the page loads.
 * 
 * Educational Note:
 * DOMContentLoaded event ensures the page is fully loaded before
 * we try to access or manipulate DOM elements.
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('The Wizard\'s Keep - Frontend Loaded');
    console.log('API URL:', CONFIG.API_BASE_URL);
    
    // Initialize the game
    Game.init();
});

/**
 * Handle page visibility changes
 * (e.g., when user switches tabs)
 */
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && Game.state.isPlaying) {
        // Reload game state when user returns to tab
        Game.loadGameState();
    }
});

/**
 * Prevent accidental page closure during gameplay
 */
window.addEventListener('beforeunload', (e) => {
    if (Game.state.isPlaying) {
        e.preventDefault();
        e.returnValue = 'Are you sure you want to leave? Your game progress is saved on the server.';
        return e.returnValue;
    }
});
