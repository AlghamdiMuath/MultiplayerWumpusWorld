#This is a class for the players in the game, it is supposed to encapsulate all the player's related data and states

class Player:
    def __init__(self, player_id, name, start_position=(0, 0)):
        self.player_id = player_id
        self.name = name
        self.position = start_position #tuble (0 <= x < 4 , 0 <= y < 4)
        self.move_count = 0            # used in the leaderboard IF the the player won
        self.is_alive = True            # Set to False if fell to a pit or killed
        self.is_spectating = False      # Set to True if fell to a pit or killed, and the spectate view is activated if true
        self.environmental_cues = {'glare': False, 'stench': False, 'breeze': False}    # For now not sure if should be maintained in then player

    def update_position(self, new_position):
        if self.is_valid_move(new_position):
            self.position = new_position
            self.move_count += 1

    def is_valid_move(self, new_position): # Check if within boarders
        row, col = new_position
        return 0 <= row < 4 and 0 <= col < 4

    def set_status(self, is_alive):     
        self.is_alive = is_alive
        if not is_alive:        # If dead, activate spectating
            self.is_spectating = True

    def update_environmental_cues(self, cues):
        self.environmental_cues.update(cues)

    def __str__(self):      # For logging and Debugging
        return (f"Player {self.player_id} - {self.name}: Position {self.position}, "
                f"Moves: {self.move_count}, Alive: {self.is_alive}, "
                f"Spectating: {self.is_spectating}, Cues: {self.environmental_cues}")
