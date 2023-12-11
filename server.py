"""
To create a more sophisticated server that serves the actual Wumpus World Multiplayer game, we can follow these steps:

1. Implement game session management to handle multiple game sessions simultaneously. This can be done by maintaining a dictionary or list of active game sessions.

2. Manage player states within a game by creating a Player class or data structure to store relevant information such as player ID, position, score, etc. Each game session can have its own list or dictionary of players.

3. Integrate game logic by implementing the rules and mechanics of the Wumpus game. This includes handling player actions, updating the game state, and determining the outcome of each turn.

4. Establish client-server communication by handling requests and responses between the server and clients. This can be achieved using sockets or a higher-level networking library. Implement protocols for joining a game, sending actions, and receiving game updates.

By considering these aspects and implementing the necessary functionality, we can create a more sophisticated server for the Wumpus World Multiplayer game.
"""


from flask import Flask, request, jsonify
from wumpus_game import WumpusGame
from player import Player

app = Flask(__name__)
game = WumpusGame()  # Initialize the game

@app.route('/move', methods=['POST'])
def move_player():
    try:
        data = request.json
        player_id = data['player_id']
        new_position = data['new_position']
        game.move_player(player_id, tuple(new_position))
        return jsonify({"message": "Move successful", "new_state": game.get_game_state()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/game_state', methods=['GET'])
def game_state():
    try:
        return jsonify(game.get_game_state()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
