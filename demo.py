import game_state
import game_viewer

if __name__=='__main__':
    state = game_state.GameState(4)
    viewer = game_viewer.GameViewer(state)
    viewer.draw_board()
    player1 = state.player_boards[0]
    v_line = player1.v_line
    for i in range(3):
        v_line.advance(0)
    for i in range(2):
        v_line.advance(1)
    viewer.draw_board()
