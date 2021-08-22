from typing import Callable


FINAL_STATE = "12345678_"


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


def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # localizar espaço em branco
    blank_position = estado.index('_')
    # testes de direção
    successors = []
    if blank_position - 3 >= 0:
        successors.append(('acima', swap_elements(estado, blank_position, blank_position - 3)))
    if blank_position + 3 <= 8:
        successors.append(('abaixo', swap_elements(estado, blank_position, blank_position + 3)))
    if (blank_position + 1) % 3 != 0:
        successors.append(('direita', swap_elements(estado, blank_position, blank_position + 1)))
    if blank_position % 3 != 0:
        successors.append(('esquerda', swap_elements(estado, blank_position, blank_position - 1)))

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

    if estado == '12345678_':
        print('O estado inicial já condiz com o objetivo')
        return []
    initial_node = Nodo(estado, None, None, 0)
    explored = []
    border = [initial_node]

    while True:
        if not estado:
            return None
        current_vertex = border.pop(0)
        if current_vertex.estado == '12345678_':
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


def astar_hamming(initial_state: str):
    return astar(initial_state, calc_hamming_estimated_cost)


def astar_manhattan(initial_state: str):
    return astar(initial_state, calc_manhattan_estimated_cost)


def astar(initial_state: str, calc_estimated_cost: Callable[[str], int]):
    initial_node = Nodo(initial_state, None, None, 0)
    border = [initial_node]
    explored = []

    try:
        while True:
            current_node = find_node_with_the_lowest_estimated_cost(border, calc_estimated_cost)
            if is_final_state(current_node.estado):
                return get_path(current_node)
            border += explore_node(current_node)
            explored.append(current_node)
    except:
        return None


def explore_node(node: Nodo) -> list[Nodo]:
    new_border_nodes = expande(node)
    for_each_node_sum_cost(new_border_nodes, node.custo)
    return new_border_nodes


# Auxiliar functions
def is_empty(list: list) -> bool:
    return not list


def is_final_state(state: str):
    return state == FINAL_STATE 


def swap_elements(string: str, fst_index: int, snd_index: int) -> str:
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


def get_path(current_vertex: Nodo) -> list:
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

    okay_chars = '12345678_'
    if not all(char in state for char in okay_chars):
        return False

    return True


def for_each_piace_sum(state: str, value_func: Callable[[str, int], int]) -> int:
    value = 0
    for posicao, peca in enumerate(state):
        value += value_func(posicao, peca)

    return value


def for_each_node_sum_cost(nodes: list[Nodo], cost: int):
    for node in nodes:
        node.custo += cost

def find_node_with_the_lowest_estimated_cost(border: list[Nodo], calc_estimated_cost: Callable[[Nodo], int]) -> Nodo:
    if is_empty(border): 
        raise Exception('Fail! Empty border.') 

    selected_node = border.pop()
    lowest_cost = calc_estimated_cost(selected_node) + selected_node.custo
    for node in border:
        node_cost = calc_estimated_cost(node) + node.custo
        if node_cost < lowest_cost:
            selected_node = node
            lowest_cost = node_cost


def calc_hamming_estimated_cost(node: Nodo) -> int:
    return for_each_piace_sum(
        node, 
        lambda piece, position: 0 if piece_is_in_the_right_position(piece, position) else 1
    )   


def piece_is_in_the_right_position(piece: str, position: int) -> bool:
    right_piece = FINAL_STATE[position]
    return piece != right_piece


def calc_manhattan_estimated_cost(node: Nodo) -> int:
    return for_each_piace_sum(
        node, 
        distance_from_the_piece_to_its_correct_position
    )        


def distance_from_the_piece_to_its_correct_position(piece: str, current_position: int) -> int: 
    right_position = FINAL_STATE.index(piece)
    return abs(right_position - current_position)