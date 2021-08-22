import constants


def play_game(initial_state: str, actions: list[str]) -> str:
    current_state = initial_state
    for action in actions:
        current_state = perform_action(current_state, action)

    return current_state


def perform_action(state: str, action: str) -> str:
    blank_position = state.index(constants.EMPTY_CHAR)
    if action == constants.UP:
        return __swap_elements(state, blank_position, blank_position - 3)
    elif action == constants.DOWN:
        return __swap_elements(state, blank_position, blank_position + 3)
    if action == constants.RIGHT:
        return __swap_elements(state, blank_position, blank_position + 1)
    elif action == constants.LEFT:
        return __swap_elements(state, blank_position, blank_position - 1)
    return state


def __swap_elements(string: str, fst_index: int, snd_index: int) -> str:
    """
    Troca dois caracteres de lugar
    :param string: palavra a ter dois caracteres trocados
    :param fst_index: index de um caracter
    :param snd_index: index do outro caracter
    :return: palavra com a troca de caracteres feita
    """
    string_list = list(string)
    string_list[fst_index], string_list[snd_index] = string_list[snd_index], string_list[fst_index]
    return ''.join(string_list)