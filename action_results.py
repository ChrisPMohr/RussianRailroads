class ActionResult(object):
    pass

class MoveTrack(ActionResult):
    def __init__(self, color, number):
        # Color is 0-4 for regular colors (black, grey, tan, natural, white),
        # -1 for any color, or -2 for black/grey
        self.color = color
        self.number = number
