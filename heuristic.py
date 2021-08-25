import utils
import constants
import math


def hamming_estimated_cost(state: str) -> int:
    """
    Função heuristíca de Hamming, baseada no número de peças fora de posição
    """
    return utils.for_each_piece_sum(
        lambda piece, position: 0 if __piece_is_in_the_right_position(piece, position) else 1,
        state
    )


def manhattan_estimated_cost(state: str) -> int:
    """
    Função heuristíca de Manhattan, baseada na distância da posição atual da peça para sua posição final
    """
    return utils.for_each_piece_sum(
        __distance_from_the_piece_to_its_correct_position,
        state
    )


def __distance_from_the_piece_to_its_correct_position(piece: str, current_position: int):
    current_cartesian_position = __convert_piece_position_to_cartesian(current_position)
    right_position = utils.get_piece_right_position_in_final_state(piece)
    right_cartesian_position = __convert_piece_position_to_cartesian(right_position)

    return __diff_cartesian_positions(
        current_cartesian_position,
        right_cartesian_position
    )


def __convert_piece_position_to_cartesian(position: int) -> tuple[int, int]:
    x = position % constants.BOARD_SIDE_SIZE
    y = position // constants.BOARD_SIDE_SIZE
    return x,y


def __diff_cartesian_positions(position_one: tuple[int, int], position_two: tuple[int, int]):
    return math.sqrt(
        pow(position_one[0] - position_two[0], 2)
        +
        pow(position_one[1] - position_two[1], 2)
)


def __piece_is_in_the_right_position(piece: str, position: int) -> bool:
    right_piece = constants.FINAL_STATE[position]
    return piece == right_piece
