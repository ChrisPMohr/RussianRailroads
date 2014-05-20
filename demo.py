import game_state
import game_viewer

if __name__=='__main__':
    state = game_state.GameState(4)
    viewer = game_viewer.GameViewer(state)
    viewer.draw_board()

    # Do one round of turns
    state.reset_board()
    ordered_players = [state.player_boards[i] for i in state.turn_order]
    board = state.game_board
    for player in ordered_players:
        if board.get_action_by_id(2).is_available():
            board.take_action(player, 2, 'ww', 'vvv')
        else:
            board.take_action(player, 12, 'w', 'bv')
        viewer.draw_board()
