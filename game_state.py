import game_board
import player_board

class GameState(object):
    """A game state consists of one game board and 2 - 4 player boards"""
    def __init__(self, player_num):
        self.player_num = player_num

        self.game_board = game_board.GameBoard(player_num)

        colors = ['red', 'blue', 'green', 'yellow']
        self.player_boards = [player_board.PlayerBoard(player_num, colors[i])
                              for i in range(player_num)]

        self.turn_order = [i for i in range(player_num)]
        self.current_turn_index = -1
        self.round = 0

    @property
    def current_player(self):
        return self.player_boards[self.turn_order[self.current_turn_index]]

    def next_round(self):
        self.round += 1
        for player in self.player_boards:
            player.reset_board()
        self.game_board.start_round()
        self.current_turn_index = -1

    def next_player(self, start = -1):
        original_index = self.current_turn_index
        self.current_turn_index += 1
        if self.current_turn_index >= len(self.turn_order):
            self.current_turn_index = 0
        if start >= -1 and self.current_turn_index == start:
            # Everyone has passed
            return -1
        elif not self.current_player.passed:
            return self.current_turn_index
        else:
            return self.next_player(start if start >= 0 else original_index)

    def player_passes(self):
        self.current_player.passed = True
        return self.next_player()
