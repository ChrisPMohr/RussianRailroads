class GameBoard(object):
    """A game board consists of many action spaces"""

    def __init__(self, num_players):
        two_player_actions = [
                ActionSpace(2, ActionCost(2, 0), MoveTrack(0, 3)),
                ReusableActionSpace(12, ActionCost(1, 0), MoveTrack(-2, 1))]

        more_player_actions = [
                ActionSpace(1, ActionCost(1, 0), MoveTrack(0, 2))]

        self.actions = two_player_actions
        if num_players > 2:
            self.actions.extend(more_player_actions)

    def get_action_by_id(self, _id):
        for action in self.actions:
            if action.id == _id:
                return action
        return None


class ActionSpace(object):
    """A space where players can place workers

    An action space has a cost and a result.
    It is either unoccupied or occupied by some workers.
    """

    def __init__(self, _id, cost, result):
        self.id = _id
        self.cost = cost
        self.cost_length = cost.workers + cost.rubles
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

class ActionResult(object):
    pass

class MoveTrack(ActionResult):
    def __init__(self, color, number):
        # Color is 0-4 for regular colors (black, grey, tan, natural, white),
        # -1 for any color, or -2 for black/grey
        self.color = color
        self.number = number
