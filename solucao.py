from typing import Callable
import constants
import action


class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado, pai, acao, custo):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.custo_estimado = 0


def sucessor(estado: str) -> tuple[str, str]:
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # localizar espaço em branco
    blank_position = estado.index(constants.EMPTY_CHAR)
    # testes de direção
    successors = []
    if blank_position - 3 >= 0:
        successors.append((
            constants.UP, 
            action.perform_action(estado, constants.UP)
        ))
    if blank_position + 3 <= 8:
        successors.append((
            constants.DOWN, 
            action.perform_action(estado, constants.DOWN)
        ))
    if (blank_position + 1) % 3 != 0:
        successors.append((
            constants.RIGHT, 
            action.perform_action(estado, constants.RIGHT)
        ))
    if blank_position % 3 != 0:
        successors.append((
            constants.LEFT, 
            action.perform_action(estado, constants.LEFT)
        ))

    return successors


def expande(nodo):
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    successors = sucessor(nodo.estado)
    return list(map(lambda successor_tuple: Nodo(successor_tuple[1], nodo, successor_tuple[0], nodo.custo + 1), successors))


def bfs(estado):
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    if not is_valid_state(estado):
        print('Estado invalido. Por favor, tente novamente')
        return

    if estado == constants.FINAL_STATE:
        print('O estado inicial já condiz com o objetivo')
        return []
    initial_node = Nodo(estado, None, None, 0)
    explored = []
    border = [initial_node]

    while True:
        if not estado:
            return None
        current_vertex = border.pop(0)
        if current_vertex.estado == constants.FINAL_STATE:
            path = get_path(current_vertex)
            return path
        explored.append(current_vertex)
        border += expande(current_vertex)


def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_hamming(initial_state: str) -> list[str]:
    return astar(initial_state, calc_hamming_estimated_cost)


def astar_manhattan(initial_state: str) -> list[str]:
    return astar(initial_state, calc_manhattan_estimated_cost)


def astar(initial_state: str, calc_estimated_cost_until_final: Callable[[str], int]) -> list[str]:
    if not is_valid_state(initial_state):
        return None

    if not is_solvable(initial_state):
        return None

    initial_node = Nodo(initial_state, None, None, 0)
    border = [initial_node]
    explored = []

    try:
        while True:
            current_node = remove_node_with_the_lowest_estimated_cost(border)
            if is_final_state(current_node.estado):
                return get_path(current_node)
            if current_node.estado not in explored:
                border += explore_node(current_node, calc_estimated_cost_until_final)
                explored.append(current_node.estado)
    except:
        return None


#region Auxiliar functions
def is_empty(list: list) -> bool:
    return not list


def is_final_state(state: str):
    return state == constants.FINAL_STATE 


def get_path(current_vertex: Nodo) -> list[str]:
    """
    Função que percorre a árvore a partir do nodo fornecido até o nodo pai inicial
    retornando uma lista com as ações que levaram até o nodo atual
    :param current_vertex: nodo atual
    :return: lista com as ações que levaram do nodo do estado inicial até o nodo atual
    """
    path = []
    while current_vertex.acao is not None:
        path.insert(0, current_vertex.acao)
        current_vertex = current_vertex.pai

    return path


def is_solvable(initial_state):
    return get_pieces_inversion_count(initial_state) % 2 == 0


def get_pieces_inversion_count(state: str):
    return for_each_piece_sum(
        lambda piece, position: get_piece_total_inversions(piece, position, state),
        state
    )


def get_piece_total_inversions(piece: str, position: int, state: str) -> int:
    return for_each_piece_sum(
        lambda successor_piece, _: 1 if are_pieces_inverted(piece, successor_piece) else 0,
        state[position + 1:]
    )


def are_pieces_inverted(piece_one: str, piece_two: str) -> bool:
    if is_empty_space(piece_one) or is_empty_space(piece_two):
        return False

    piece_one_right_position = get_piece_right_position_in_final_state(piece_one)
    piece_two_right_position = get_piece_right_position_in_final_state(piece_two)
    return piece_one_right_position > piece_two_right_position


def get_piece_right_position_in_final_state(piece):
    return constants.FINAL_STATE.find(piece)


def is_empty_space(piece: str) -> bool:
    return piece == constants.EMPTY_CHAR


def is_valid_state(state: str) -> bool:
    """
    Função que avalia se um estado é válido ou não
    Para um estado ser válido, é necessário tem 9 caracteres, sendo um de cada um dos valores 1-8 + '_'
    :param state: estado a ser verificado
    :return: booleano indicando se o estado é válido ou não
    """
    if len(state) != 9:
        return False

    okay_chars = constants.FINAL_STATE
    if not all(char in state for char in okay_chars):
        return False

    return True


#region Auxiliar cost calculation function    

def for_each_piece_sum(value_func: Callable[[str, int], int], state: str) -> int:
    value = 0
    for position, piece in enumerate(state):
        value += value_func(piece, position)

    return value


def calc_hamming_estimated_cost(state: str) -> int:
    return for_each_piece_sum(
        lambda piece, position: 0 if piece_is_in_the_right_position(piece, position) else 1,
        state
    )   


def piece_is_in_the_right_position(piece: str, position: int) -> bool:
    right_piece = constants.FINAL_STATE[position]
    return piece == right_piece


def calc_manhattan_estimated_cost(state: str) -> int:
    return for_each_piece_sum(
        distance_from_the_piece_to_its_correct_position,
        state
    )        


def distance_from_the_piece_to_its_correct_position(piece: str, current_position: int) -> int: 
    right_position = get_piece_right_position_in_final_state(piece)
    return abs(right_position - current_position)


#endregion


#region Auxiliar node cost function

def for_each_node_set_cost(cost: int, nodes: list[Nodo]):
    for node in nodes:
        node.custo = cost


def for_each_node_set_estimated_cost(calc_estimated_cost: Callable[[Nodo], int], nodes: list[Nodo]):
    for node in nodes:
        node.custo_estimado = calc_estimated_cost(node)


def remove_node_with_the_lowest_estimated_cost(nodes: list[Nodo]) -> Nodo:
    if is_empty(nodes): 
        raise Exception('Fail! Empty border.') 

    selected_node = nodes[0]
    for node in nodes[1:]:
        if node.custo_estimado < selected_node.custo_estimado:
            selected_node = node
            
    nodes.remove(selected_node)
    return selected_node


def explore_node(origin_node: Nodo, calc_estimated_cost_until_final: Callable[[str], int]) -> list[Nodo]:
    new_border_nodes = expande(origin_node)
    new_nodes_cost = origin_node.custo + 1
    for_each_node_set_cost(
        new_nodes_cost,
        new_border_nodes
    )
    for_each_node_set_estimated_cost(
        lambda node: calc_estimated_cost_until_final(node.estado) + new_nodes_cost,
        new_border_nodes
    )
    return new_border_nodes

#endregion

#endregion