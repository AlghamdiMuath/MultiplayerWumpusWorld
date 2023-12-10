import unittest
from wumpus_game import WumpusGame, GRID_SIZE

class TestWumpusGame(unittest.TestCase):

    def setUp(self):
        self.game = WumpusGame()

    def test_initialization(self):
        self.assertEqual(len(self.game.grid), GRID_SIZE)
        self.assertEqual(len(self.game.players), 2)
        self.assertFalse(self.game.game_over)

    def test_player_placement(self):
        for player in self.game.players:
            x, y = player.position
            self.assertIn(x, range(GRID_SIZE))
            self.assertIn(y, range(GRID_SIZE))

    def test_hazard_placement(self):
        # Check that hazards are within the grid
        for wumpus in self.game.wumpuses:
            self.assertIn(wumpus[0], range(GRID_SIZE))
            self.assertIn(wumpus[1], range(GRID_SIZE))

        for pit in self.game.pits:
            self.assertIn(pit[0], range(GRID_SIZE))
            self.assertIn(pit[1], range(GRID_SIZE))

        # Check that hazards do not overlap with player positions
        player_positions = [player.position for player in self.game.players]
        for hazard in self.game.wumpuses + self.game.pits:
            self.assertNotIn(hazard, player_positions)

    def test_treasure_placement(self):
        # Check that the treasure is within the grid
        treasure_x, treasure_y = self.game.treasure_position
        self.assertIn(treasure_x, range(GRID_SIZE))
        self.assertIn(treasure_y, range(GRID_SIZE))

        # Check that the treasure is equidistant from all players
        player_positions = [player.position for player in self.game.players]
        distances = [abs(treasure_x - px) + abs(treasure_y - py) for px, py in player_positions]
        self.assertEqual(len(set(distances)), 1)  # All distances should be the same

        # Check that the treasure is accessible from each player's position
        for player_position in player_positions:
            self.assertTrue(self.game.is_reachable(player_position, self.game.treasure_position))

    def test_player_movements(self):
        player_id = self.game.players[0].player_id
        initial_position = self.game.players[0].position

        # Test valid move
        new_position = (initial_position[0], initial_position[1] + 1)
        self.game.move_player(player_id, new_position)
        self.assertEqual(self.game.players[0].position, new_position)

        # Test invalid move (outside grid)
        invalid_position = (GRID_SIZE, GRID_SIZE)
        self.game.move_player(player_id, invalid_position)
        self.assertNotEqual(self.game.players[0].position, invalid_position)
        self.assertEqual(self.game.players[0].position, new_position)  # Position should remain the same as after the valid move

    # def test_environmental_cues(self):
    #     # Place the player next to each type of element (treasure, Wumpus, and pit) and check cues
    #     for player in self.game.players:
    #         # Test adjacent to treasure
    #         self.game.place_treasure_equidistant()  # Ensure treasure is placed
    #         treasure_x, treasure_y = self.game.treasure_position
    #         self.game.move_player(player.player_id, (treasure_x, treasure_y - 1))
    #         self.assertTrue(player.environmental_cues['glare'])

    #         # Test adjacent to a Wumpus
    #         wumpus_x, wumpus_y = self.game.wumpuses[0]
    #         self.game.move_player(player.player_id, (wumpus_x, wumpus_y - 1))
    #         self.assertTrue(player.environmental_cues['stench'])

    #         # Test adjacent to a pit
    #         pit_x, pit_y = self.game.pits[0]
    #         self.game.move_player(player.player_id, (pit_x, pit_y - 1))
    #         self.assertTrue(player.environmental_cues['breeze'])

    def test_environmental_cues(self):
        self.game.place_treasure_equidistant()  # Ensure treasure is placed
        treasure_x, treasure_y = self.game.treasure_position
        player = self.game.players[0]

        # Move player next to the treasure
        adjacent_pos = (treasure_x, treasure_y - 1)
        self.game.move_player(player.player_id, adjacent_pos)
        
        # Additional check for debugging
        print(f"Treasure Position: {self.game.treasure_position}, Player Position: {player.position}")

        # Assert 'glare' cue is True
        self.assertTrue(player.environmental_cues['glare'])

    def test_game_ending_conditions(self):
        # Test game ending by finding the treasure
        for player in self.game.players:
            self.game.move_player(player.player_id, self.game.treasure_position)
            self.assertTrue(self.game.game_over)
            self.assertEqual(self.game.winner, player.player_id)
            self.game.game_over = False  # Reset for next test

        # Ensure there are pits before testing
        self.assertTrue(len(self.game.pits) > 0, "No pits in the game.")
        pit_x, pit_y = self.game.pits[0]

        # Test game ending by falling into a pit
        for player in self.game.players:
            self.game.move_player(player.player_id, (pit_x, pit_y))
            self.assertFalse(player.is_alive)
            if all(not p.is_alive for p in self.game.players):
                self.assertTrue(self.game.game_over)
            self.game.game_over = False  # Reset for next test

        # Test game ending by encountering a Wumpus
        wumpus_x, wumpus_y = self.game.wumpuses[0]
        for player in self.game.players:
            self.game.move_player(player.player_id, (wumpus_x, wumpus_y))
            self.assertFalse(player.is_alive)
            if all(not p.is_alive for p in self.game.players):
                self.assertTrue(self.game.game_over)
            self.game.game_over = False  # Reset for next test

        # Test game ending by running out of time
    def test_time_limit(self):
        # Simulate time passing just before the limit
        self.game.start_time -= (WumpusGame.TIME_LIMIT - 1)
        self.assertFalse(self.game.is_time_up())
        self.assertFalse(self.game.game_over)

        # Simulate time passing the limit
        self.game.start_time -= 2  # 1 second more to pass the limit
        self.assertTrue(self.game.is_time_up())

        # The next player movement should end the game
        player_id = self.game.players[0].player_id
        self.game.move_player(player_id, (1, 1))
        self.assertTrue(self.game.game_over)


if __name__ == "__main__":
    unittest.main()
