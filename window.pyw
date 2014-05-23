import game_state
from action_widget import ActionWidget

import sys
from PyQt4 import QtGui


default_style = 'font-size: 10pt; font-family: Courier;'

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.init_UI()

    def init_UI(self):
        self.state = game_state.GameState(
            4, ['Alice', 'Bob', 'Carol', 'Dave'])

        # Set up the board layout
        overall_layout = QtGui.QGridLayout()

        # Show round info
        self.round_label = QtGui.QLabel('Round info')
        overall_layout.addWidget(self.round_label, 1, 1)

        # Set up action spaces
        self.action_widget = ActionWidget(self)
        overall_layout.addWidget(self.action_widget, 3, 1)

        # Set up the player boards
        all_player_layout = QtGui.QGridLayout()
        self.players = list()

        for i in range(self.state.player_num):
            player = UIPlayer(self.state.player_boards[i])
            self.players.append(player)
            all_player_layout.addLayout(player.layout, 2, i + 1)

        self.current_player_label = QtGui.QLabel('')
        all_player_layout.addWidget(self.current_player_label, 1, 1)
        self.current_player = None

        self.start_round()

        overall_layout.addLayout(all_player_layout, 4, 1, 1, -1)

        self.setLayout(overall_layout)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Russian Railroads')
        self.show()

    def start_round(self):
        self.state.next_round()
        self.next_player()
        # update round label
        self.refresh_round_label()
        # refresh action layout
        self.action_widget.refresh_layout()
        # refresh player layouts
        for player in self.players:
            player.refresh_layout()

    def refresh_round_label(self):
        state = self.state
        turn_order = [state.player_boards[state.turn_order[i]].name
                      for i in range(state.player_num)]
        turn_order_string = ' - '.join(turn_order)
        label_string = 'Round {} Turn Order: {}'.format(
            state.round, turn_order_string)
        self.round_label.setText(label_string)

    def next_player(self):
        self.set_current_player(self.state.next_player())

    def set_current_player(self, new_current_player):
        self.current_player = self.players[new_current_player]
        self.current_player_label.setText(
            'Current Player: ' + self.current_player.board.color)


class UIPlayer(object):
    def __init__(self, player_board):
        self.board = player_board
        self.layout = PlayerLayout(player_board)

    def refresh_layout(self):
        self.layout.refresh_layout(self.board)


class PlayerLayout(QtGui.QGridLayout):
    def __init__(self, player_board, parent=None):
        super(PlayerLayout, self).__init__(parent)
        self.init_layout(player_board)
        self.refresh_layout(player_board)

    def init_layout(self, player_board):
        header = "{} ({})".format(player_board.color.upper(), player_board.name)
        self.header_label = QtGui.QLabel(header)
        self.worker_label = QtGui.QLabel()
        self.worker_label.setStyleSheet(default_style)
        self.train_label = QtGui.QLabel()
        self.train_label.setStyleSheet(default_style)


        self.addWidget(self.header_label, 1, 1)
        self.addWidget(self.worker_label, 2, 1)
        self.addWidget(self.train_label, 3, 1)
        self.setRowStretch(4,1)

    def refresh_layout(self, player_board):
        workers = [('w', player_board.color) for _ in range(player_board.workers)]
        rubles = [('$', player_board.color) for _ in range(player_board.rubles)]
        self.worker_label.setText(worker_string(workers + rubles))
        self.train_label.setText(all_trains_string(player_board))


def worker_string(workers):
    return ''.join(color[0] if symbol == 'w' else symbol
                   for symbol, color in workers)


def all_trains_string(player_board):
    label_string = '\n'.join([
        train_line_string('V', player_board.v_line),
        train_line_string('S', player_board.s_line),
        train_line_string('K', player_board.k_line)])
    return label_string


def train_line_string(name, train_line):
    return_string = name
    color_letters = 'BGTNW'
    for i, color_count in enumerate(train_line.colors):
        if color_count > 0:
            return_string += ' ' + str(color_count) + color_letters[i]
    return return_string


def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
