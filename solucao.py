ESTADO_OBJETIVO = "12345678_"


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
        print(f'Nodo criado: {self.estado} a partir do nodo {self.pai}')


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


def swap_elements(string, blank_index, new_blank_position):
    string_list = list(string)
    string_list[blank_index], string_list[new_blank_position] = string_list[new_blank_position], string_list[blank_index]
    return ''.join(string_list)


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
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


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


def distancia_de_hamming(estado: str) -> int:
    distancia = 0
    for posicao, peca in enumerate(estado):
        if peca_esta_na_posicao_errada(peca, posicao):
            distancia += 1

    return distancia


def peca_esta_na_posicao_errada(peca: str, posicao: int) -> bool:
    peca_correta = ESTADO_OBJETIVO[posicao]
    return peca != peca_correta


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


def distancia_manhattan(estado: str) -> int:
    distancia = 0
    for posicao, peca in enumerate(estado):
        distancia += distancia_da_peca_a_sua_posicao_correta(peca, posicao)

    return distancia


def distancia_da_peca_a_sua_posicao_correta(peca: str, posicao_atual: int) -> int: 
    posicao_correta = ESTADO_OBJETIVO.index(peca)
    return abs(posicao_correta - posicao_atual)

