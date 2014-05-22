from action_results import MoveTrack
import action_taker

class GameBoard(object):
    """A game board consists of many action spaces and a turn order"""

    def __init__(self, num_players):
        two_player_actions = [
            ActionSpace(2, ActionCost(2, 0), MoveTrack(0, 3)),
            ActionSpace(4, ActionCost(2, 0), MoveTrack(1, 3)),
            ReusableActionSpace(12, ActionCost(1, 0), MoveTrack(-2, 1))]

        more_player_actions = [
            ActionSpace(1, ActionCost(1, 0), MoveTrack(0, 2)),
            ActionSpace(3, ActionCost(1, 0), MoveTrack(1, 2))]

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

    def is_available(self):
        if self.occupants:
            return False
        else:
            return True

class ReusableActionSpace(ActionSpace):
    def is_available(self):
        return True

class ActionCost(object):
    """The cost of an action in workers and rubles"""
    def __init__(self, workers, rubles):
        self.workers = workers
        self.rubles = rubles
