from dlgo import gotypes
from termcolor import colored

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    gotypes.Player.black: ' X ',
    gotypes.Player.white: ' O ',
}

STONE_TO_COLOR = {
    None: 'white',
    gotypes.Player.black: 'red',
    gotypes.Player.white: 'green',
    'last_move': 'magenta',
}


def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))


def print_board(board, last_move=None):
    for row in range(board.num_rows, 0, -1):
        bump = ' ' if row <= 9 else ''  # to make sure all numbers are right justified (other ways to do this)
        line = []
        for col in range(1, board.num_cols + 1):
            current_point = gotypes.Point(row=row, col=col)
            stone = board.get(current_point)
            stone_color = STONE_TO_COLOR[stone]
            if last_move is not None and last_move.is_play and current_point == last_move.point:
                stone_color = STONE_TO_COLOR['last_move']
            line.append(colored(STONE_TO_CHAR[stone], stone_color))
        print('%s%d %s' % (bump, row, ''.join(line)))
    print('    ' + '  '.join(COLS[:board.num_cols]))
