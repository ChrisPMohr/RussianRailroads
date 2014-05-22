import train_line

class PlayerBoard(object):
    """A player's personal board

    A player board consists of three lines and a player's supply, which
    include workers, rubles, and other player possessions
    """

    def __init__(self, num_players, color):
        self.color = color
        self.passed = False

        # Set up train lines
        self.v_line = train_line.VladivostokLine()
        self.s_line = train_line.StPetersburgLine()
        self.k_line = train_line.KievLine()

        # Set up workers
        if num_players == 2:
            self.max_workers = 6
        else:
            self.max_workers = 5
        self.workers = self.max_workers
#       Add special workers back in later
#        self.max_special_workers = 0
#        self.temporary_workers = 0
        self.rubles = 1

    def reset_board(self):
        self.passed = False
        self.workers = self.max_workers
