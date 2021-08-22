from typing import Callable
import constants

def is_solvable(initial_state):
    """
    Verifica se um estado inicial possui solução.
    Para isto é necessário verificar se o número de inversões no estado é par.
    Uma inversão é dada por cada par de peças onde uma peça "menor" está a frente de uma "maior"
    Exemplo:
        1 2 3
        4 5 _
        8 6 7
    Neste caso temos duas inversões, (8,6) e (8,7).
    """
    return __get_pieces_inversion_count(initial_state) % 2 == 0


def for_each_piece_sum(value_func: Callable[[str, int], int], state: str) -> int:
    """
    Retorna a soma dos valores geradores pela execução da função de entrada sobre cada par (peça, posição)
    """
    value = 0
    for position, piece in enumerate(state):
        value += value_func(piece, position)

    return value


def get_piece_right_position_in_final_state(piece):
    """
    Retorna a posição da peça no estado final
    """
    return constants.FINAL_STATE.find(piece)


def is_blank_space(piece: str) -> bool:
    """
    Verifica se a peça é o espaço em branco
    """
    return piece == constants.EMPTY_CHAR


def is_empty_list(list: list) -> bool:
    """
    Verifica se a lista é vazia
    """
    return not list


def is_final_state(state: str):
    """
    Verifica se o estado é final
    """
    return state == constants.FINAL_STATE 


def __get_pieces_inversion_count(state: str):
    return for_each_piece_sum(
        lambda piece, position: __get_piece_total_inversions(piece, position, state),
        state
    )


def __get_piece_total_inversions(piece: str, position: int, state: str) -> int:
    return for_each_piece_sum(
        lambda successor_piece, _: 1 if __are_pieces_inverted(piece, successor_piece) else 0,
        state[position + 1:]
    )


def __are_pieces_inverted(piece_one: str, piece_two: str) -> bool:
    if is_blank_space(piece_one) or is_blank_space(piece_two):
        return False

    piece_one_right_position = get_piece_right_position_in_final_state(piece_one)
    piece_two_right_position = get_piece_right_position_in_final_state(piece_two)
    return piece_one_right_position > piece_two_right_position