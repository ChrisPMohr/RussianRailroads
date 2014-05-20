import game_board
import player_board

class GameState(object):
    """A game state consists of one game board and 2 - 4 player boards"""
    def __init__(self, player_num):
        self.player_num = player_num
        self.game_board = game_board.GameBoard(player_num)
        self.player_boards = [player_board.PlayerBoard(player_num)
                              for _ in range(player_num)]

        self.turn_order = [i for i in range(player_num)]
