import numpy as np

TARGET_BOARD = '12345678_'
BOARD_SIZE = (3, 3)
SPACE_CHAR = '_'

MOVE_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


class InvalidBoard(Exception):
    pass


def check_board(board, target_board=TARGET_BOARD):
    if not isinstance(board, str):
        raise InvalidBoard("Invalid board, has to be a string")
    if not len(board) == len(target_board):
        raise InvalidBoard(f"Invalid board, needs to be {len(target_board)} characters long")
    if False in [c in board for c in target_board]:
        raise InvalidBoard(f"Invalid board, can only be a rearrangement of '{target_board}'")
    return


def locate_in_space(board, space_char=SPACE_CHAR, board_size=BOARD_SIZE):
    check_board(board)
    linear_position = board.index(space_char)
    return linear_position // board_size[0], linear_position % board_size[0]


def get_linear_position(location, board_size=BOARD_SIZE):
    return board_size[0]*location[0] + location[1]


def swap_elements(board, location, direction, board_size=BOARD_SIZE):
    first_linear_position = get_linear_position(location)
    second_linear_position = get_linear_position([sum(x) for x in zip(location,direction)])
    first = first_linear_position
    second = second_linear_position
    if second <= first:
        first = second_linear_position
        second = first_linear_position
    return board[:first] + board[second] + board[first+1:second] + board[first] + board[second+1:]


class InvalidDimensions(Exception):
    pass


def can_move(location, offset, board_size=BOARD_SIZE):
    if len(location) != len(offset):
        raise InvalidDimensions("Invalid input, 'location' and 'offset' must be of same dimension")
    for dimension in range(len(location)):
        if location[dimension] + offset[dimension] >= board_size[dimension]:
            return False
        if location[dimension] + offset[dimension] < 0:
            return False
    return True

#def move(board, location, offset, board_size+BOARD_SIZE):


def successor(board, move_directions=MOVE_DIRECTIONS):
    check_board(board)
    location = locate_in_space(board)
    successors = []
    for direction in move_directions:
        if can_move(location, direction):
            successors.append(swap_elements(board, location, direction))
    return successors


print(successor("123_46785"))

