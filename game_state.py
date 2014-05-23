import game_board
import player_board

class GameState(object):
    """A game state consists of one game board and 2 - 4 player boards"""
    def __init__(self, player_num, names):
        self.player_num = player_num

        self.game_board = game_board.GameBoard(player_num, self)

        colors = ['red', 'blue', 'green', 'yellow']
        self.player_boards = [
            player_board.PlayerBoard(player_num, names[i], colors[i])
            for i in range(player_num)]

        self.turn_order = [i for i in range(player_num)]
        self.current_turn_index = -1
        self.worker_replacement_order = []
        self.next_turn_order = self.turn_order

        self.round = 0
        self.all_players_passed = False

    @property
    def current_player(self):
        """The player board of the current player"""
        return self.player_boards[self.turn_order[self.current_turn_index]]

    def next_round(self):
        """Finished the current round and resets the board for the next
           one.
        """
        self.turn_order = self.next_turn_order
        self.round += 1
        for player in self.player_boards:
            player.reset_board()
        self.game_board.start_round()
        self.current_turn_index = -1
        self.all_players_passed = False

    def next_player(self, start=-1):
        """Returns the index of the next player to move"""
        if not self.all_players_passed:
            original_index = self.current_turn_index
            self.current_turn_index += 1

            # Loop through players in player order, skipping
            # players who passed
            if self.current_turn_index >= len(self.turn_order):
                self.current_turn_index = 0
            if start >= -1 and self.current_turn_index == start:
                # Everyone has passed
                self.all_players_passed = True
                # Set next turn order
                self.set_next_turn_order()
                # Generate order for moving pieces off of turn order spaces
                self.set_worker_replacement_order()
                return self.next_player()
            elif not self.current_player.passed:
                return self.turn_order[self.current_turn_index]
            else:
                return self.next_player(
                    start if start >= 0 else original_index)
        else:
            if self.worker_replacement_order:
                return self.worker_replacement_order.pop(0)
            else:
                return -1

    def player_passes(self):
        """Sets a player as having passed the round and returns the
           index of the next player to move
        """
        self.current_player.passed = True
        return self.next_player()

    def set_next_turn_order(self):
        """Set the turn order for next round"""
        turn_order_spaces = game_board.TurnOrderActionSpace.all_spaces

        # Find the occupants of the turn order spaces
        first_space = None
        second_space = None
        for space in turn_order_spaces:
            if turn_order_space_number(space) == 0:
                first_space = space
            elif turn_order_space_number(space) == 1:
                second_space = space

        # Modify the turn order
        next_turn_order = list(self.turn_order)
        # first space player
        if first_space.occupants:
            index = self.occupant_player_index(first_space.occupants)
            next_turn_order.remove(index)
            next_turn_order.insert(0, index)

        # second space player
        if second_space and second_space.occupants:
            index = self.occupant_player_index(second_space.occupants)
            if not first_space.occupants and self.turn_order[0] == index:
                # Special case if the first player is the only one to
                # change the player order, their position doesn't get worse
                pass
            else:
                next_turn_order.remove(index)
                next_turn_order.insert(1, index)

        self.next_turn_order = next_turn_order


    def set_worker_replacement_order(self):
        """Set the order of players to move their pieces off the turn
           selection spaces
        """
        turn_order_spaces = game_board.TurnOrderActionSpace.all_spaces
        turn_order_spaces.sort(key=turn_order_space_number, reverse=True)
        self.worker_replacement_order = [
            self.occupant_player_index(space.occupants)
            for space in turn_order_spaces
            if self.occupant_player_index(space.occupants) is not None]

    def player_index_with_color(self, color):
        """Returns the index of the player with the given color"""
        for i, player in enumerate(self.player_boards):
            if player.color == color:
                return i
        return -1

    def occupant_player_index(self, occupants):
        if occupants:
            color = occupants[0][1]
            return self.player_index_with_color(color)

def turn_order_space_number(space):
    """Returns the number of the given turn number action space"""
    return space.result.number
