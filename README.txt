Problemas a resolver:
    -quando faz moove, tem de atualizar a lista das posições ocupadas no Ambiente
    -criar o agente tem de ser depois dos obstáculos (ou seja, o ambiente já existe) para se usar a função freePositions
    -coordenada inicial do agente: Como resolver o facto de não conseguiromos saber que posições estão livres?  




implementar 2 modos 
    -aprendizagem
        .Q-learning
        .Genético
    -teste
        .politica fixa



Ambient
    Attributes:
        - agents: list[Agent]
        - obstacles: list[Obstacle]
        - lighthouse: LightHouse
        - grid_size (or bounds): tuple[int,int] / whatever represents limits
        - occupied_positions: set[Coord] or similar
    Methods:
#       - freePositions() -> list[Coord]
        - getLightHouse() -> LightHouse
        - getAgentsList() -> list[Agent]
#       - render() -> str (render)

Agent
    Attributes:
        - name: str
        - coord: Coord
        - ambient: Ambient
        - finished_flag: bool
    Methods:
        - getCoord() -> Coord
        - getName() -> str
        - move(destination: Coord) -> None
        - finished() -> None
        - isFinished() -> bool
        - nextMove(freePositions: Iterable[Coord]) -> None
        - getLightHouseDirection() -> tuple[float,float]  (or Vector)

LightHouse
    Attributes:
        - coord: Coord
    Methods:
        - getCoord() -> Coord

Obstacle
    Attributes:
        - coord: Coord
    Methods:
        - getCoord() -> Coord

Coord
    Attributes:
        - x: int
        - y: int
    Methods:
        - getX() -> int
        - getY() -> int
        - setX(x: int) -> None
        - setY(y: int) -> None
        - __eq__(other) -> bool
        - __repr__() / __str__() -> str
        - distance_to(other: Coord) -> float
        - as_tuple() -> tuple[int,int]

#######################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$################################################


mapa inicial (já a pensar no obstáculos) será descrito num ficheiro txt/JSon.
Posição inicial dos agentes: Aleatoria. temos de fazer todos-ocupados

# Agente P — Resumo do projeto

Descrição
- Projeto de simulação multiagente (Agente P). Ambiente discreto com obstáculos e um farol (LightHouse).
- Mapa inicial será lido de ficheiro (txt ou JSON). Posições iniciais dos agentes são aleatórias (garantir sem colisões).

Modelo de domínio (classes principais)
- Coord: coordenadas x,y; distância, equals, toString.
- Vector: dx,dy; normalização, escala, produto interno.
- Obstacle: posição (Coord).
- LightHouse: posição, alcance, direção (opcional).
- Agent: id, posição, velocidade, estado finished, memória (Map); métodos para calcular/praticar próximo passo.
- Ambient: tamanho (width, height), listas de agentes e obstáculos, farol; verifica ocupação e calcula posições livres.

Formato do mapa (sugestão)
- JSON simples contendo width, height, lista de obstáculos (x,y) e opcional configuração do farol.
    Exemplo:
    {
        "width": 20,
        "height": 15,
        "obstacles": [{"x":3,"y":4}, {"x":7,"y":10}],
        "lighthouse": {"x":10,"y":2,"range":5}
    }
- Alternativa: ficheiro txt linha a linha (formato definido conforme necessidade).

Inicialização de agentes
- Colocar N agentes em posições aleatórias escolhidas a partir de freePositions() do Ambient.
- Garantir unicidade: sortear posições sem reposição até preencher o número de agentes.

Como executar (simples)
- Código Java puro, sem dependências externas.
- Compilar: javac *.java
- Executar: java Main (implementar Main que carrega mapa, inicializa Ambient e agentes e corre iterações).

Próximos passos / TODO
- Implementar leitura/escrita JSON e validação do mapa.
- Melhorar comportamento dos agentes: pathfinding (A*), detecção/evitação de colisões, comunicação entre agentes.
- Simulação tempo-step com resolução de conflitos (quando dois agentes querem a mesma célula).
- UI/visualização (console, Swing ou export para CSV/JSON para análise).
- Testes unitários e exemplos de mapas.

Contribuição
- Documentar funções públicas e formatos de ficheiro.
- Abrir issues para funcionalidades e bugs.

Licença
- Definir licença (ex: MIT) no repositório.


#######################################################################################################################################




