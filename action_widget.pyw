from PyQt4 import QtGui

default_style = 'font-size: 10pt; font-family: Courier;'

class ActionWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ActionWidget, self).__init__()
        self.parent = parent
        self.state = parent.state
        self.init_widget()

    def init_widget(self):
        layout = QtGui.QGridLayout()

        # Set up the action spaces
        self.actions = list()
        action_2b = ActionButton('[{:<1}] -> 2B', 1, self)
        action_3b = ActionButton('[{:<2}] -> 3B', 2, self)
        action_2g = ActionButton('[{:<1}] -> 2G', 3, self)
        action_3g = ActionButton('[{:<2}] -> 3G', 4, self)
        action_1b_or_1g = ActionButton('[{:<6}] -> 1B/1G', 12, self)

        pass_button = QtGui.QPushButton('Pass')
        pass_button.clicked.connect(self.handle_pass_button)

        layout.addWidget(action_2b, 1, 1, 1, 2)
        layout.addWidget(action_3b, 1, 3, 1, 2)
        layout.addWidget(action_2g, 2, 1, 1, 2)
        layout.addWidget(action_3g, 2, 3, 1, 2)
        layout.addWidget(action_1b_or_1g, 3, 1, 1, 4)

        layout.addWidget(pass_button, 1, 5)

        layout.setColumnStretch(10, 1)
        self.setLayout(layout)

    def handle_action_button(self):
        sender = self.sender()
        board = self.state.game_board
        action = sender.action
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
                    self.parent.current_player.board,
                    action, payment, choices)
                self.parent.current_player.refresh_layout()
                sender.refresh_button()
                self.parent.next_player()

    def handle_pass_button(self):
        next_player = self.state.player_passes()
        if next_player == -1:
            QtGui.QMessageBox.about(
                self, 'Turn Over',
                'All players passed. The turn is over.')
            self.parent.start_round()
        else:
            self.parent.set_current_player(next_player)

    def refresh_layout(self):
        for action in self.actions:
            action.refresh_button()


class ActionButton(QtGui.QPushButton):
    def __init__(self, action_format, _id, parent=None):
        super(ActionButton, self).__init__(parent)
        self.clicked.connect(parent.handle_action_button)
        parent.actions.append(self)

        self.action = parent.state.game_board.get_action_by_id(_id)
        self.action_format = action_format

        self.setStyleSheet(default_style)
        self.refresh_button()

    def refresh_button(self):
        occupant_symbols = occupant_string(self.action.occupants)
        self.setText(self.action_format.format(occupant_symbols))

def occupant_string(occupants):
    return ''.join(color[0] if symbol == 'w' else symbol
                   for symbol, color in occupants)
