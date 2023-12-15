// Store the current player position (initially set to box 7)
const adjacent_list = {1: [2, 5],
              2: [1, 3, 6],
              3: [2, 4, 7],
              4: [3, 8],
              5: [1, 6, 9],
              6: [2, 5, 7, 10],
              7: [3, 6, 8, 11],
              8: [4, 7, 12],
              9: [5, 10, 13],
              10: [6, 9, 11, 14],
              11: [7, 10, 12, 15],
              12: [8, 11, 16],
              13: [9, 14],
              14: [10, 13, 15],
              15: [11, 14, 16],
              16: [12, 15]};

const socket = io('http://192.168.1.103:5000');
let currentPlayerId; // Variable to store the current player's ID

socket.on('player_id', (data) => {
    currentPlayerId = data.player_id;
    console.log("Received Player ID: ", currentPlayerId);
    // Now you can use currentPlayerId in your game logic
});
socket.on('connect', () => {
    console.log('Connected to the server');
});


// Handle disconnect event
socket.on('disconnect', () => {
    console.log('Disconnected from the server');
    // Handle disconnection logic...
});

function handleGridClick(event) {
    console.log(event.target.id);
    if (currentPlayerId) {
        const moveData = {
            player_id: currentPlayerId,
            new_position: event.target.id
        };
        socket.emit('move', moveData);
    } else {
        console.error("Player ID is not set.");
    }
}

function updateGrid(new_state) {
    boxes = document.getElementsByClassName('grid-item');
    for (let i = 0; i < boxes.length; i++) {
        boxes[i].innerHTML = new_state.grid[Math.floor(i/4)][i%4];
    }
}
// Handle move update event
socket.on('move_update', (data) => {
    console.log('Move successful', data.new_state);
    // Update your game UI based on the new state...
    updateGrid(data.new_state);
});

// Handle move error event
socket.on('move_error', (error) => {
    console.error('Move error', error.error);
    // Handle error feedback...
});

// Example of requesting the game state
// socket.emit('game_state');

// Handle game state update event
socket.on('game_state_update', (data) => {
    console.log('Game state update', data);
    // Update your game UI based on the new state...
});

// Handle game state error event
socket.on('game_state_error', (error) => {
    console.error('Game state error', error.error);
    // Handle error feedback...
});

socket.on('player_joined', (data) => {
    console.log(data.message);
    // Update the UI to reflect that a new player has joined.
});

socket.on('waiting_for_opponent', (data) => {
    console.log(data.message);
    // Update the UI to show that the player is waiting for an opponent.
});

socket.on('join_error', (error) => {
    console.error(error.error);
    // Display an error message to the user.
});

document.getElementById('startGameBtn').addEventListener('click', function() {
    console.log("Start Game button clicked. Emitting 'play_game' event.");
    socket.emit('play_game');
});

socket.on('game_started', (data) => {
    console.log(data.message);
       // Here, you can request the player ID and the game state
    // socket.emit('request_player_id');
    socket.emit('game_state');
    console.log("Requesting player ID and game state.");
    window.location.href = '/index.html'; // Redirects to the game interface
});
socket.on('game_state_update', (data) => {
    updateGrid(data.new_state); // Example function to update the UI based on the new game state
});
