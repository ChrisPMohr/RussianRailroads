import game_state
import game_viewer

if __name__=='__main__':
    state = game_state.GameState(4)
    viewer = game_viewer.GameViewer(state)
    viewer.draw_board()

    player1 = state.player_boards[0]
    board = state.game_board

    board.take_action(player1, 2, 'vvv')
    viewer.draw_board()

    board.take_action(player1, 12, 'gv')
    board.take_action(player1, 12, 'gv')
    board.take_action(player1, 12, 'gv')
    board.take_action(player1, 12, 'bv')
    board.take_action(player1, 12, 'gv')
    viewer.draw_board()
