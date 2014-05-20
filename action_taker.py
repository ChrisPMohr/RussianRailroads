from action_results import MoveTrack
import game_exceptions

class ActionTaker(object):
    def take_action(self, player, action, input_string):
        result = action.result
        result_type = type(result)
        if result_type is MoveTrack:
            action_color = result.color
            track_number = result.number
            if action_color >= 0:
                # parse input as a order to advance tracks
                if len(input_string) == track_number:
                    for line in input_string:
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
                if len(input_string) == track_number * 2:
                    string_iter = iter(input_string)
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
