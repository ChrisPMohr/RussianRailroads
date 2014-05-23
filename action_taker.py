from action_results import MoveTrack, TurnOrder
import game_exceptions

class ActionTaker(object):
    def __init__(self, state):
        self.state = state

    def take_action(self, player, action, payment_input, result_input):
        # check is space is available
        if not action.is_available(player):
            raise game_exceptions.InvalidMoveError(
                'Action space is not available')

        # translate the payment_input
        num_workers = 0
        num_rubles = 0
        for letter in payment_input:
            if letter == 'w':
                num_workers += 1
            elif letter == '$':
                num_rubles += 1
            else:
                raise game_exceptions.BadInputError('Invalid payment')

        # if the action is being taken after all players have passed,
        # it can only be paid for with a reloacted worker
        if self.state.all_players_passed:
            if num_workers != 1 or num_rubles != 0:
                raise game_exceptions.InvalidMoveError(
                    'Cannot combine any other payment with relocated worker')
            if isinstance(action, TurnOrder):
                raise game_exceptions.InvalidMoveError(
                    'Cannot take turn order action after next turn\'s'
                    'order has been determined')

        # check if player can pay input
        if ((player.workers < num_workers or player.rubles < num_rubles) and
                not self.state.all_players_passed):
            raise game_exceptions.InvalidMoveError(
                'Player cannot afford payment')

        # check if input meets cost
        cost = action.cost
        if (cost.rubles > num_rubles or
                cost.workers + cost.rubles != num_workers + num_rubles):
            raise game_exceptions.InvalidMoveError(
                'Not enough paid for action')

        # apply action
        result = action.result
        result_type = type(result)
        if result_type is MoveTrack:
            move_track(player, result, result_input)

        # make player pay cost for action
        if not self.state.all_players_passed:
            player.workers -= num_workers
            player.rubles -= num_rubles

        # fill action slot with workers
        for _ in range(num_workers):
            action.occupants.append(('w', player.color))
        for _ in range(num_rubles):
            action.occupants.append(('$', player.color))

def move_track(player, result, result_input):
    action_color = result.color
    track_number = result.number
    if action_color >= 0:
        # parse input as a order to advance tracks
        if len(result_input) == track_number:
            for line in result_input:
                if line == 'v':
                    player.v_line.advance(action_color)
                elif line == 's':
                    player.s_line.advance(action_color)
                elif line == 'k':
                    player.k_line.advance(action_color)
                else:
                    raise game_exceptions.BadInputError(
                        'Invalid track name')
        else:
            raise game_exceptions.BadInputError('Wrong input length')
    else:
        # parse input as color, track name pairs
        if len(result_input) == track_number * 2:
            string_iter = iter(result_input)
            for color, line in zip(string_iter, string_iter):
                colors = {'b': 0, 'g': 1, 't': 2, 'n': 3, 'w': 4}
                try:
                    input_color = colors[color]
                except KeyError:
                    raise game_exceptions.BadInputError(
                        'Invalid color name')
                if action_color == -2 and input_color > 1:
                    raise game_exceptions.BadInputError(
                        'Invalid color for this action')
                if line == 'v':
                    player.v_line.advance(input_color)
                elif line == 's':
                    player.s_line.advance(input_color)
                elif line == 'k':
                    player.k_line.advance(input_color)
                else:
                    raise game_exceptions.BadInputError(
                        'Invalid track name')
        else:
            raise game_exceptions.BadInputError('Wrong input length')
