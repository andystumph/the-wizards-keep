/**
 * Game Module
 * 
 * Manages game state and UI interactions.
 * 
 * Educational Notes:
 * - Module pattern encapsulates related functionality
 * - Separation between data (state) and presentation (UI)
 * - Event-driven architecture for user interactions
 */

const Game = {
    // Game state
    state: {
        playerId: null,
        playerName: null,
        characterName: null,
        currentLocation: null,
        health: 100,
        maxHealth: 100,
        level: 1,
        isPlaying: false
    },

    // Command history for up/down arrow navigation
    commandHistory: [],
    historyIndex: -1,

    /**
     * Initialize the game
     */
    init() {
        console.log('Initializing The Wizard\'s Keep...');
        this.bindEvents();
        this.checkApiConnection();
    },

    /**
     * Check if API is accessible
     */
    async checkApiConnection() {
        const isConnected = await API.healthCheck();
        if (!isConnected) {
            this.displayError('Cannot connect to game server. Please ensure the backend is running.');
        }
    },

    /**
     * Bind UI event listeners
     */
    bindEvents() {
        // Start game button
        const startBtn = document.getElementById('start-game');
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startGame());
        }

        // Enter key on character creation
        const usernameInput = document.getElementById('username');
        const charnameInput = document.getElementById('charname');
        
        [usernameInput, charnameInput].forEach(input => {
            if (input) {
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.startGame();
                    }
                });
            }
        });

        // Command input
        const commandInput = document.getElementById('command-input');
        if (commandInput) {
            commandInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleCommand();
                }
            });

            // Command history navigation (up/down arrows)
            commandInput.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    this.navigateHistory('up');
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    this.navigateHistory('down');
                }
            });
        }

        // Quick command buttons
        const quickBtns = document.querySelectorAll('.quick-btn');
        quickBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const command = btn.getAttribute('data-command');
                this.executeCommand(command);
            });
        });
    },

    /**
     * Start a new game
     */
    async startGame() {
        const username = document.getElementById('username').value.trim();
        const characterName = document.getElementById('charname').value.trim();

        // Validation
        if (!username) {
            alert('Please enter a username');
            return;
        }

        if (!characterName) {
            alert('Please enter a character name');
            return;
        }

        // Show loading
        this.displayMessage('Creating your character...');

        // Create player via API
        const result = await API.players.create(username, characterName);

        if (!result.success) {
            alert(`Error creating player: ${result.error}`);
            return;
        }

        // Store player info
        this.state.playerId = result.data.id;
        this.state.playerName = username;
        this.state.characterName = characterName;
        this.state.isPlaying = true;

        // Switch to game screen
        document.getElementById('welcome-screen').style.display = 'none';
        document.getElementById('game-screen').style.display = 'flex';

        // Update UI
        document.getElementById('player-name').textContent = characterName;

        // Clear output and show intro
        this.clearOutput();
        this.displayMessage('═══════════════════════════════════════════════════', 'accent');
        this.displayMessage(`Welcome, ${characterName}!`, 'success');
        this.displayMessage('═══════════════════════════════════════════════════', 'accent');
        this.displayMessage('');

        // Load initial game state
        await this.loadGameState();

        // Auto-look around
        await this.executeCommand('LOOK');

        // Focus on input
        document.getElementById('command-input').focus();
    },

    /**
     * Load current game state from server
     */
    async loadGameState() {
        const result = await API.players.getGameState(this.state.playerId);

        if (result.success) {
            const gameState = result.data;
            this.state.health = gameState.health;
            this.state.maxHealth = gameState.max_health;
            this.state.level = gameState.current_level;

            this.updateStatusBar();
        }
    },

    /**
     * Handle command input
     */
    async handleCommand() {
        const input = document.getElementById('command-input');
        const command = input.value.trim().toUpperCase();

        if (!command) return;

        // Add to history
        this.commandHistory.push(command);
        if (this.commandHistory.length > CONFIG.COMMAND_HISTORY_SIZE) {
            this.commandHistory.shift();
        }
        this.historyIndex = this.commandHistory.length;

        // Clear input
        input.value = '';

        // Execute command
        await this.executeCommand(command);
    },

    /**
     * Navigate command history
     */
    navigateHistory(direction) {
        if (this.commandHistory.length === 0) return;

        const input = document.getElementById('command-input');

        if (direction === 'up') {
            if (this.historyIndex > 0) {
                this.historyIndex--;
                input.value = this.commandHistory[this.historyIndex];
            }
        } else if (direction === 'down') {
            if (this.historyIndex < this.commandHistory.length - 1) {
                this.historyIndex++;
                input.value = this.commandHistory[this.historyIndex];
            } else {
                this.historyIndex = this.commandHistory.length;
                input.value = '';
            }
        }
    },

    /**
     * Execute a game command
     */
    async executeCommand(command) {
        if (!this.state.isPlaying) return;

        // Display command in output
        this.displayMessage(`> ${command}`, 'command');

        // Handle local commands
        if (command === 'CLEAR') {
            this.clearOutput();
            return;
        }

        // Send to API
        const result = await API.game.sendCommand(this.state.playerId, command);

        if (result.success) {
            const response = result.data;

            // Display message
            if (response.message) {
                const messageType = response.success ? 'normal' : 'error';
                this.displayMessage(response.message, messageType);
            }

            // Update game state if provided
            if (response.game_state) {
                this.state.health = response.game_state.health;
                this.state.maxHealth = response.game_state.max_health;
                this.state.level = response.game_state.current_level;
                this.updateStatusBar();
            }

            // Update location if provided
            if (response.location) {
                this.state.currentLocation = response.location.name;
                document.getElementById('location-name').textContent = response.location.name;
            }

            // Check for game completion
            if (response.game_state && response.game_state.is_completed) {
                this.displayMessage('');
                this.displayMessage('═══════════════════════════════════════════════════', 'accent');
                this.displayMessage('🎉 CONGRATULATIONS! YOU HAVE COMPLETED THE QUEST! 🎉', 'success');
                this.displayMessage('═══════════════════════════════════════════════════', 'accent');
            }
        } else {
            this.displayMessage(`Error: ${result.error}`, 'error');
        }

        this.displayMessage(''); // Blank line for spacing
    },

    /**
     * Update status bar
     */
    updateStatusBar() {
        document.getElementById('health-value').textContent = 
            `${this.state.health}/${this.state.maxHealth}`;
        document.getElementById('level-value').textContent = 
            `${this.state.level}/3`;
    },

    /**
     * Display message in output area
     */
    displayMessage(text, type = 'normal') {
        const output = document.getElementById('output');
        const line = document.createElement('div');
        line.className = 'output-line';

        if (type === 'command') {
            line.classList.add('command');
        } else if (type === 'error') {
            line.classList.add('error');
        } else if (type === 'success') {
            line.classList.add('success');
        } else if (type === 'accent') {
            line.classList.add('text-accent');
        }

        line.textContent = text;
        output.appendChild(line);

        // Auto-scroll to bottom
        if (CONFIG.AUTO_SCROLL) {
            output.scrollTop = output.scrollHeight;
        }
    },

    /**
     * Display error message
     */
    displayError(text) {
        this.displayMessage(`ERROR: ${text}`, 'error');
    },

    /**
     * Clear output area
     */
    clearOutput() {
        const output = document.getElementById('output');
        output.innerHTML = '';
    }
};

// Make Game available globally
window.Game = Game;
