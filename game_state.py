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
        self.reset_board()

    def reset_board(self):
        for player in self.player_boards:
            player.reset_board()
        self.current_turn_index = -1

    def next_player(self):
        self.current_turn_index += 1
        if self.current_turn_index >= len(self.turn_order):
            self.current_turn_index = 0
        return self.current_turn_index
