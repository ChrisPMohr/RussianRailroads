from PyQt4 import QtGui
from PyQt4 import QtCore

default_style = 'font-size: 10pt; font-family: Courier;'

class ActionWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ActionWidget, self).__init__()
        self.parent = parent
        self.state = parent.state
        self.init_widget()

    def init_widget(self):
        layout = QtGui.QGridLayout()

        self.actions = list()

        # Populate track layout
        track_layout = QtGui.QGridLayout()
        action_2b = ActionButton('[{:<1}] -> 2B', 1, self)
        action_3b = ActionButton('[{:<2}] -> 3B', 2, self)
        action_2g = ActionButton('[{:<1}] -> 2G', 3, self)
        action_3g = ActionButton('[{:<2}] -> 3G', 4, self)
        action_1b_or_1g = ActionButton('[{:<6}] -> 1B/1G', 12, self)

        track_layout.addWidget(action_2b, 1, 1, 1, 2)
        track_layout.addWidget(action_3b, 1, 3, 1, 2)
        track_layout.addWidget(action_2g, 2, 1, 1, 2)
        track_layout.addWidget(action_3g, 2, 3, 1, 2)
        track_layout.addWidget(action_1b_or_1g, 3, 1, 1, 4)

        # Populate turn order layout
        turn_order_layout = QtGui.QGridLayout()

        # Add turn order labels
        self.color_order_labels = list()

        for i in range(self.state.player_num):
            number_label = SizedLabel(str(i), 80, 20)
            turn_order_layout.addWidget(number_label, 1, i + 1)

            color_label = SizedLabel('', 80, 20)
            turn_order_layout.addWidget(color_label, 2, i + 1)
            self.color_order_labels.append(color_label)

        action_1st = ActionButton('[{:<1}]', 13, self)
        turn_order_layout.addWidget(action_1st, 3, 1)
        if self.state.player_num > 2:
            action_2nd = ActionButton('[{:<2}]', 14, self)
            turn_order_layout.addWidget(action_2nd, 3, 2)

        pass_button = QtGui.QPushButton('Pass')
        pass_button.clicked.connect(self.handle_pass_button)
        turn_order_layout.addWidget(pass_button, 4, 1, 1, -1)

        layout.addLayout(track_layout, 1, 1)
        layout.addLayout(turn_order_layout, 1, 2)
        layout.setColumnStretch(3, 1)

        self.setLayout(layout)

    def handle_action_button(self):
        sender = self.sender()
        board = self.state.game_board
        action = sender.action
        player = self.parent.current_player.board
        if action and action.is_available(player):
            # open dialog for text payment and choices input
            payment, ok_payment = QtGui.QInputDialog.getText(
                self, 'Payment Input',
                'Enter Payment:')

            choices, ok_choices = QtGui.QInputDialog.getText(
                self, 'Choices Input',
                'Enter Choices:')

            if ok_payment and ok_choices:
                board.take_action(player, action, payment, choices)
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
        for i, label in enumerate(self.color_order_labels):
            label.setText(self.state.player_boards[
                self.state.turn_order[i]].color[0].upper())


class ActionButton(QtGui.QPushButton):
    def __init__(self, action_format, _id, parent):
        super(ActionButton, self).__init__(parent)
        self.clicked.connect(parent.handle_action_button)
        parent.actions.append(self)

        self.action = parent.state.game_board.get_action_by_id(_id)
        self.action_format = action_format

        self.setStyleSheet(default_style)
        self.refresh_button()

    def refresh_button(self):
        if self.action:
            occupant_symbols = occupant_string(self.action.occupants)
        else:
            occupant_symbols = ''
        self.setText(self.action_format.format(occupant_symbols))

class SizedLabel(QtGui.QLabel):
    def __init__(self, text, width, height, parent=None):
        super(SizedLabel, self).__init__(text, parent)
        self._width = width
        self._height = height
        self.setSizePolicy(QtGui.QSizePolicy.Minimum,
                           QtGui.QSizePolicy.Minimum)

    def sizeHint(self):
        return QtCore.QSize(self._width, self._height)

def occupant_string(occupants):
    return ''.join(color[0] if symbol == 'w' else symbol
                   for symbol, color in occupants)
