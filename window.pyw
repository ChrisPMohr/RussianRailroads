import game_state

import sys
from PyQt4 import QtGui


default_style = 'font-size: 10pt; font-family: Courier;'

class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.init_UI()

    def init_UI(self):
        self.state = game_state.GameState(3)

        # Set up the board layout
        overall_layout = QtGui.QGridLayout()

        # Set up the action spaces
        action1 = ActionButton('[{:<1}] -> 2B', 1, self)
        action2 = ActionButton('[{:<2}] -> 3B', 2, self)
        action3 = ActionButton('[{:<6}] -> 1B/1G', 12, self)

        action1.clicked.connect(self.handle_action_button)
        action2.clicked.connect(self.handle_action_button)
        action3.clicked.connect(self.handle_action_button)

        overall_layout.addWidget(action1, 1, 1)
        overall_layout.addWidget(action2, 2, 1)
        overall_layout.addWidget(action3, 3, 1)

        overall_layout.setColumnStretch(2, 1)

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
        self.next_player()


        overall_layout.addLayout(all_player_layout, 4, 1, 1, 2)

        self.setLayout(overall_layout)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Russian Railroads')
        self.show()

    def handle_action_button(self):
        print('button clicked')
        sender = self.sender()
        _id = sender.id
        board = self.state.game_board
        action = self.state.game_board.get_action_by_id(_id)
        if action and action.is_available():
            # open dialog for text payment and choices input
            payment, ok_payment = QtGui.QInputDialog.getText(
                    self, 'Payment Input',
                    'Enter Payment:')

            choices, ok_choices = QtGui.QInputDialog.getText(
                    self, 'Choices Input',
                    'Enter Choices:')

            if ok_payment and ok_choices:
                board.take_action(
                        self.current_player.board,
                        _id, payment, choices)
                self.current_player.refresh_layout()
                sender.format_text(action.occupants)
                self.next_player()

    def next_player(self):
        self.current_player = self.players[self.state.next_player()]
        self.current_player_label.setText('Current Player: ' + self.current_player.board.color)

class ActionButton(QtGui.QPushButton):
    def __init__(self, action_format, _id, parent=None):
        super(ActionButton, self).__init__(parent)
        self.id = _id
        self.action_format = action_format

        self.setStyleSheet(default_style)
        self.format_text()

    def format_text(self, occupants=[]):
        occupant_symbols = worker_string(occupants)
        self.setText(self.action_format.format(occupant_symbols))


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
        self.color_label = QtGui.QLabel(player_board.color)
        self.worker_label = QtGui.QLabel()
        self.worker_label.setStyleSheet(default_style)
        self.train_label = QtGui.QLabel()
        self.train_label.setStyleSheet(default_style)


        self.addWidget(self.color_label, 1, 1)
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
