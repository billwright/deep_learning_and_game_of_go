from dlgo.agent import naive
from dlgo import game_state
from dlgo import gotypes
from dlgo.utils import print_move, print_board
import time


def main():
    board_size = 9
    game = game_state.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: naive.RandomBot(),
        gotypes.Player.white: naive.RandomBot()
    }
    bot_move = None
    while not game.is_over():
        time.sleep(0.3)

        print_board(game.board, bot_move)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()
