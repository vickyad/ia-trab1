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


def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


# Auxiliar functions
def swap_elements(string, blank_index, new_blank_position):
    string_list = list(string)
    string_list[blank_index], string_list[new_blank_position] = string_list[new_blank_position], string_list[blank_index]
    return ''.join(string_list)


def get_path(current_vertex):
    path = []
    while current_vertex.acao is not None:
        path.insert(0, current_vertex.acao)
        current_vertex = current_vertex.pai

    return path


def is_valid_state(state):
    if len(state) != 9:
        return False

    okay_chars = '12345678_'
    if not all(char in state for char in okay_chars):
        return False

    return True
