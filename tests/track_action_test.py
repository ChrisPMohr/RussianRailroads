"""Tests for the actions that extend tracks"""

import unittest
from unittest.mock import Mock

import game_state
import game_exceptions

class Action2BTests(unittest.TestCase):
    def setUp(self):
        self.state = game_state.GameState(4, ['A', 'B', 'C', 'D'])
        self.game_board = self.state.game_board
        self.player = self.state.player_boards[0]

    def test_2b_action_v_line(self):
        action = self.game_board.get_action_by_id(1)
        self.game_board.take_action(self.player, action, 'w', 'vv')
        self.assertEqual(self.player.v_line.colors,
                         [3, 0, 0, 0, 0])
        self.assertEqual(self.player.s_line.colors,
                         [1, 0, 0, 0])
        self.assertEqual(self.player.k_line.colors,
                         [1, 0, 0])

    def test_2b_action_s_line(self):
        action = self.game_board.get_action_by_id(1)
        self.game_board.take_action(self.player, action, 'w', 'ss')
        self.assertEqual(self.player.v_line.colors,
                         [1, 0, 0, 0, 0])
        self.assertEqual(self.player.s_line.colors,
                         [3, 0, 0, 0])
        self.assertEqual(self.player.k_line.colors,
                         [1, 0, 0])

    def test_2b_action_k_line(self):
        action = self.game_board.get_action_by_id(1)
        self.game_board.take_action(self.player, action, 'w', 'kk')
        self.assertEqual(self.player.v_line.colors,
                         [1, 0, 0, 0, 0])
        self.assertEqual(self.player.s_line.colors,
                         [1, 0, 0, 0])
        self.assertEqual(self.player.k_line.colors,
                         [3, 0, 0])

    def test_2b_action_split(self):
        action = self.game_board.get_action_by_id(1)
        self.game_board.take_action(self.player, action, 'w', 'vs')
        self.assertEqual(self.player.v_line.colors,
                         [2, 0, 0, 0, 0])
        self.assertEqual(self.player.s_line.colors,
                         [2, 0, 0, 0])
        self.assertEqual(self.player.k_line.colors,
                         [1, 0, 0])

    def test_2b_action_not_enough_paid(self):
        action = self.game_board.get_action_by_id(1)
        with self.assertRaises(game_exceptions.InvalidMoveError):
            self.game_board.take_action(self.player, action, '', 'vv')

    def test_2b_action_too_much_paid(self):
        action = self.game_board.get_action_by_id(1)
        with self.assertRaises(game_exceptions.InvalidMoveError):
            self.game_board.take_action(self.player, action, 'ww', 'vv')


    def test_2b_action_cannot_afford(self):
        action = self.game_board.get_action_by_id(12)
        self.game_board.take_action(self.player, action, '$', 'bv')
        self.assertEqual(self.player.v_line.colors,
                         [2, 0, 0, 0, 0])
        self.assertEqual(self.player.s_line.colors,
                         [1, 0, 0, 0])
        self.assertEqual(self.player.k_line.colors,
                         [1, 0, 0])
        action = self.game_board.get_action_by_id(1)
        with self.assertRaises(game_exceptions.InvalidMoveError):
            self.game_board.take_action(self.player, action, '$', 'vv')


if __name__ == '__main__':
    unittest.main()
