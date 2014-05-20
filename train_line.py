from game_exceptions import InvalidMoveError

class TrainLine(object):
    def advance(self, color):
        # Can only advance if the color is valid
        if color >= 0 and color < len(self.colors):
            # Can only advance if won't pass end of the line
            if self.colors[color] < self.length:
                # Can only advance if the next color isn't in the way
                if (color == 0 or
                    self.colors[color - 1] > self.colors[color] + 1):
                    # Sucessfully advance track
                    self.colors[color] += 1
                else:
                    raise InvalidMoveError('Tried to pass next color track')
            else:
                raise InvalidMoveError(
                    'Tried to move track past the end of the line')
        else:
            raise InvalidMoveError('Invalid color')


class VladivostokLine(TrainLine):
    def __init__(self):
        self.colors = [1, 0, 0, 0, 0]
        self.length = 15

class StPetersburgLine(TrainLine):
    def __init__(self):
        self.colors = [1, 0, 0, 0]
        length = 9

class KievLine(TrainLine):
    def __init__(self):
        self.colors = [1, 0, 0]
        length = 9
