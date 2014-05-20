class GameViewer(object):
    def __init__(self, game_state):
        self.game_state = game_state

    def draw_board(self):
        print('-' * 40)

        # Draw game board
        self.draw_action('[{:<1}]-> 2B', 1)
        self.draw_action('[{:<2}]-> 3B', 2)
        self.draw_action('[{:<6}]-> 1B/1G', 12)

        # Draw player boards
        for player_board in self.game_state.player_boards:
            print()
            print(self.draw_train_line('V', player_board.v_line))
            print(self.draw_train_line('S', player_board.s_line))
            print(self.draw_train_line('K', player_board.k_line))

        print('-' * 40)

    def draw_action(self, format_string, _id):
        action = self.game_state.game_board.get_action_by_id(_id)
        if action:
            workers = ''.join(color if symbol == 'w' else symbol
                              for symbol, color in action.occupants)
            print(format_string.format(workers))
        else:
            return ' ' * len(format_string.format(''))


    def draw_train_line(self, name, train_line):
        return_string = name
        color_letters = 'BGTNW'
        for i, color_count in enumerate(train_line.colors):
            if color_count > 0:
                return_string += ' ' + str(color_count) + color_letters[i]
        return return_string
