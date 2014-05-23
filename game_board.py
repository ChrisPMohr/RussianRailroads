from action_results import MoveTrack, TurnOrder
import action_taker

class GameBoard(object):
    """A game board consists of many action spaces and a turn order"""

    def __init__(self, num_players, state):
        two_player_actions = [
            ActionSpace(2, ActionCost(2, 0), MoveTrack(0, 3)),
            ActionSpace(4, ActionCost(2, 0), MoveTrack(1, 3)),
            ReusableActionSpace(12, ActionCost(1, 0), MoveTrack(-2, 1)),
            TurnOrderActionSpace(13, ActionCost(1, 0), TurnOrder(0), state)]

        more_player_actions = [
            ActionSpace(1, ActionCost(1, 0), MoveTrack(0, 2)),
            ActionSpace(3, ActionCost(1, 0), MoveTrack(1, 2)),
            TurnOrderActionSpace(14, ActionCost(1, 0), TurnOrder(1), state)]

        self.actions = two_player_actions
        if num_players > 2:
            self.actions.extend(more_player_actions)

        self.action_taker = action_taker.ActionTaker()

    def get_action_by_id(self, _id):
        for action in self.actions:
            if action._id == _id:
                return action
        return None

    def take_action(self, player, action, cost_input, result_input):
        self.action_taker.take_action(player, action,
                                      cost_input, result_input)

    def start_round(self):
        for action in self.actions:
            action.occupants = []

class ActionSpace(object):
    """A space where players can place workers

    An action space has a cost and a result.
    It is either unoccupied or occupied by some workers.
    """

    def __init__(self, _id, cost, result):
        self._id = _id
        self.cost = cost
        self.result = result
        self.occupants = []

    def is_available(self, player):
        if self.occupants:
            return False
        else:
            return True

class ReusableActionSpace(ActionSpace):
    def is_available(self, player):
        return True

class TurnOrderActionSpace(ActionSpace):
    all_spaces = dict()

    def __init__(self, _id, cost, result, state):
        super(TurnOrderActionSpace, self).__init__(_id, cost, result)
        ordinal = result.number
        self.all_spaces[ordinal] = self
        self.state = state

    def is_available(self, player):
        # check that player doesn't already occupy the other turn order space
        for number, space in self.all_spaces.items():
            if space.occupants and space.occupants[0][1] == player.color:
                return False

        # check that player isn't currently in that position
        # or that it is a 2 player game.
        ordinal = self.result.number
        position_current_player = self.state.player_boards[
            self.state.turn_order[ordinal]]
        if self.state.player_num > 2 and player == position_current_player:
            return False
        else:
            return super(TurnOrderActionSpace, self).is_available(player)

class ActionCost(object):
    """The cost of an action in workers and rubles"""
    def __init__(self, workers, rubles):
        self.workers = workers
        self.rubles = rubles
