from typing import Callable
import constants
import action
import heuristic
import utils


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
    return list(
        map(lambda successor_tuple: Nodo(successor_tuple[1], nodo, successor_tuple[0], nodo.custo + 1), successors))


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
        print('Estado inicial invalido. Por favor, tente novamente')
        return None

    if not utils.is_solvable(estado):
        print('Estado inicial não solucionável. Por favor, tente novamente')
        return None

    if estado == constants.FINAL_STATE:
        print('O estado inicial já condiz com o objetivo')
        return []

    initial_node = Nodo(estado, None, None, 0)
    explored = set()
    border = [initial_node]

    while border:
        current_vertex = border.pop(0)
        if current_vertex.estado == constants.FINAL_STATE:
            path = get_path(current_vertex)
            return path

        if current_vertex.estado not in explored:
            explored.add(current_vertex.estado)
            border += expande(current_vertex)
    return None


def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    if not is_valid_state(estado):
        print('Estado invalido. Por favor, tente novamente')
        return

    initial_node = Nodo(estado, None, None, 0)
    explored = []
    border = [initial_node]

    visitados = []
    while True:
        if not border:
            return None
        current_vertex = border.pop()
        if current_vertex.estado == constants.FINAL_STATE:
            path = get_path(current_vertex)
            return path
        if current_vertex.estado not in visitados:
            explored.append(current_vertex)
            visitados.append(current_vertex.estado)
            border += expande(current_vertex)


def astar_hamming(initial_state: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param initial_state:
    :return:
    """
    return __astar(initial_state, heuristic.hamming_estimated_cost)


def astar_manhattan(initial_state: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :return:
    """
    return __astar(initial_state, heuristic.manhattan_estimated_cost)


def __astar(initial_state: str, calc_heuristic_cost: Callable[[str], int]) -> list[str]:
    if not is_valid_state(initial_state):
        return None

    if not utils.is_solvable(initial_state):
        return None

    initial_node = Nodo(initial_state, None, None, 0)
    border = [initial_node]
    explored = []

    try:
        while True:
            current_node = __remove_node_with_the_lowest_estimated_cost(border)
            if utils.is_final_state(current_node.estado):
                return get_path(current_node)
            if current_node.estado not in explored:
                border += __explore_node(current_node, calc_heuristic_cost)
                explored.append(current_node.estado)
    except:
        return None


# region Auxiliar functions
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


def __for_each_node_set_cost(cost: int, nodes: list[Nodo]):
    for node in nodes:
        node.custo = cost


def __for_each_node_set_estimated_cost(calc_estimated_cost: Callable[[Nodo], int], nodes: list[Nodo]):
    for node in nodes:
        node.custo_estimado = calc_estimated_cost(node)


def __remove_node_with_the_lowest_estimated_cost(nodes: list[Nodo]) -> Nodo:
    if utils.is_empty_list(nodes):
        raise Exception('Fail! Empty border.')

    selected_node = nodes[0]
    for node in nodes[1:]:
        if node.custo_estimado < selected_node.custo_estimado:
            selected_node = node

    nodes.remove(selected_node)
    return selected_node


def __explore_node(origin_node: Nodo, calc_heuristic_cost: Callable[[str], int]) -> list[Nodo]:
    new_border_nodes = expande(origin_node)
    new_nodes_cost = origin_node.custo + 1
    __for_each_node_set_cost(
        new_nodes_cost,
        new_border_nodes
    )
    __for_each_node_set_estimated_cost(
        lambda node: calc_heuristic_cost(node.estado) + new_nodes_cost,
        new_border_nodes
    )
    return new_border_nodes

# endregion
