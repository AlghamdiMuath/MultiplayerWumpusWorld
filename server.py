import uuid

def generate_unique_id():
    return str(uuid.uuid4())

from flask import Flask, render_template
from flask_socketio import SocketIO

from threading import Lock

from wumpus_game import WumpusGame
from flask import request
from player import Player
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
game_instances = {}
game_instance_lock = Lock()
PLAYERS_TO_START = 2  # Define minimum number of players to start a game

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    player = Player()

    # Assign player to an existing game instance or create a new one
    game_instance_id = find_available_game_instance() or create_game_instance()
    WumpusGame.get_game(game_instance_id).add_player(id(player), player.name)

    if WumpusGame.get_game(game_instance_id).is_ready_to_start():
        WumpusGame.get_game(game_instance_id).start_game()

    socketio.emit('game_data', {
        "game_instance_id": game_instance_id, 
        "player_id": id(player), 
        "game_state": WumpusGame.get_game(game_instance_id).get_player_pov_game_state(id(player))
    })

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    # Handle client disconnection logic here...
    for game_instance_id, game_instance in game_instances.items():
        for player in game_instance.players:
            if id(player) == request.sid:
                game_instance.players.remove(player)
                break

@socketio.on('move')
def handle_move(data):
    try:
        player_id = data['player_id']
        new_position = data['new_position']
        
        # Find the game instance that the player belongs to
        game_instance_id = None
        for id, instance in game_instances.items():
            if player_id in [id(p) for p in instance.players]:
                game_instance_id = id
                break
        
        if game_instance_id:
            # Handle move logic and emit updates to clients in the same game instance
            WumpusGame.get_game(game_instance_id).move_player(player_id, new_position)
            game_state = WumpusGame.get_game(game_instance_id).get_player_pov_game_state(player_id)
            for player in WumpusGame.get_game(game_instance_id).players:
                socketio.emit('move_update', {"message": "Move successful", "new_state": game_state}, room=id(player))
        else:
            raise Exception("Player not found in any game instance")
    
    except Exception as e:
        print(str(e))
        socketio.emit('move_error', {"error": str(e)})

def find_available_game_instance():
    for game_instance_id, game_instance in game_instances.items():
        if len(game_instance.players) < PLAYERS_TO_START and not game_instance.game_over:
            return game_instance_id
    return None

def create_game_instance():
    game_instance_id = generate_unique_id()  # Unique ID generation logic
    game_instances[game_instance_id] = WumpusGame(game_instance_id)
    return game_instance_id

@socketio.on('game_state')
def handle_game_state():
    try:
        player_id = request.sid
        game_instance_id = None
        for id, instance in game_instances.items():
            if player_id in [id(p) for p in instance.players]:
                game_instance_id = id
                break
        
        if game_instance_id:
            game_state = WumpusGame.get_game(game_instance_id).get_player_pov_game_state(player_id)
            socketio.emit('game_state_update', game_state, room=player_id)
        else:
            raise Exception("Player not found in any game instance")
    
    except Exception as e:
        socketio.emit('game_state_error', {"error": str(e)})
@app.route('/')
def index():
    return render_template('mainmenu.html')
@app.route('/mainmenu.html')
def index():
    return render_template('mainmenu.html')

@app.route('/game.html')
def game():
    return render_template('index.html')  # Added ".html"

@app.route('/createlobby.html')
def createlobby():
    return render_template('createlobby.html')

@app.route('/joinlobby.html')
def joinlobby():
    return render_template('joinlobby.html')

@app.route('/startgame.html')
def startgame():
    return render_template('startgame.html')

@app.route('/leaderboard.html')
def leaderboard():
    return render_template('leaderboard.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
