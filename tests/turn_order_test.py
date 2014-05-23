"""Tests for the actions that extend tracks"""

import unittest

import game_state
import game_exceptions

class TurnOrderTests(unittest.TestCase):
    def setUp(self):
        self.state = game_state.GameState(4, ['A', 'B', 'C', 'D'])

    def test_next_player(self):
        self.assertEqual(self.state.next_player(), 0)
        self.assertEqual(self.state.next_player(), 1)
        self.assertEqual(self.state.next_player(), 2)
        self.assertEqual(self.state.next_player(), 3)
        self.assertEqual(self.state.next_player(), 0)

    def test_next_player_different_turn_order(self):
        self.state.turn_order = [3, 2, 1, 0]
        self.assertEqual(self.state.next_player(), 3)
        self.assertEqual(self.state.next_player(), 2)
        self.assertEqual(self.state.next_player(), 1)
        self.assertEqual(self.state.next_player(), 0)
        self.assertEqual(self.state.next_player(), 3)

    def test_one_player_pass(self):
        self.assertEqual(self.state.next_player(), 0)
        self.assertEqual(self.state.next_player(), 1)
        self.assertEqual(self.state.player_passes(), 2)
        self.assertEqual(self.state.next_player(), 3)
        self.assertEqual(self.state.next_player(), 0)
        self.assertEqual(self.state.next_player(), 2)

    def test_all_players_pass(self):
        self.assertEqual(self.state.next_player(), 0)
        self.assertEqual(self.state.player_passes(), 1)
        self.assertEqual(self.state.player_passes(), 2)
        self.assertEqual(self.state.player_passes(), 3)
        self.assertFalse(self.state.all_players_passed)
        self.state.player_passes()
        self.assertTrue(self.state.all_players_passed)

    def test_all_players_pass_different_turn_order(self):
        self.state.turn_order = [3, 2, 1, 0]
        self.assertEqual(self.state.next_player(), 3)
        self.assertEqual(self.state.player_passes(), 2)
        self.assertEqual(self.state.player_passes(), 1)
        self.assertEqual(self.state.player_passes(), 0)
        self.assertFalse(self.state.all_players_passed)
        self.assertEqual(self.state.player_passes(), -1)
        self.assertTrue(self.state.all_players_passed)


class ChangeTurnOrderTests(unittest.TestCase):
    def setUp(self):
        self.state = game_state.GameState(4, ['A', 'B', 'C', 'D'])
        self.game_board = self.state.game_board

    def test_move_player_two_to_first(self):
        action = self.game_board.get_action_by_id(13)
        player = self.state.player_boards[1]
        self.game_board.take_action(player, action, 'w', '')
        self.all_pass()
        self.assertEqual(self.state.next_player(), 1)
        self.assertEqual(self.state.next_player(), -1)
        self.state.next_round()
        self.assertEqual(self.state.turn_order, [1, 0, 2, 3])

    def test_move_player_four_to_first(self):
        action = self.game_board.get_action_by_id(13)
        player = self.state.player_boards[3]
        self.game_board.take_action(player, action, 'w', '')
        self.all_pass()
        self.assertEqual(self.state.next_player(), 3)
        self.assertEqual(self.state.next_player(), -1)
        self.state.next_round()
        self.assertEqual(self.state.turn_order, [3, 0, 1, 2])

    def test_move_player_three_to_second(self):
        action = self.game_board.get_action_by_id(14)
        player = self.state.player_boards[2]
        self.game_board.take_action(player, action, 'w', '')
        self.all_pass()
        self.assertEqual(self.state.next_player(), 2)
        self.assertEqual(self.state.next_player(), -1)
        self.state.next_round()
        self.assertEqual(self.state.turn_order, [0, 2, 1, 3])

    def test_move_player_one_to_second(self):
        action = self.game_board.get_action_by_id(14)
        player = self.state.player_boards[0]
        self.game_board.take_action(player, action, 'w', '')
        self.all_pass()
        self.assertEqual(self.state.next_player(), 0)
        self.assertEqual(self.state.next_player(), -1)
        self.state.next_round()
        self.assertEqual(self.state.turn_order, [0, 1, 2, 3])

    def test_move_player_two_to_first_and_player_three_to_second(self):
        action = self.game_board.get_action_by_id(13)
        player = self.state.player_boards[1]
        self.game_board.take_action(player, action, 'w', '')

        action = self.game_board.get_action_by_id(14)
        player = self.state.player_boards[2]
        self.game_board.take_action(player, action, 'w', '')

        self.all_pass()
        self.assertEqual(self.state.next_player(), 2)
        self.assertEqual(self.state.next_player(), 1)
        self.assertEqual(self.state.next_player(), -1)
        self.state.next_round()
        self.assertEqual(self.state.turn_order, [1, 2, 0, 3])

    def all_pass(self):
        self.assertEqual(self.state.next_player(), 0)
        self.assertEqual(self.state.player_passes(), 1)
        self.assertEqual(self.state.player_passes(), 2)
        self.assertEqual(self.state.player_passes(), 3)

if __name__ == '__main__':
    unittest.main()
