import networkx as nx

START = '#'
END = '$'
WALL = '-'


class Graph():
    '''
    graph: networkx graph
    rows: number of rows
    cols: number of columns
    start: tuple containing start coordinates
    end: tuple containing end coordinates
    '''

    def __init__(self, input_matrix):
        '''
        Return Networkx graph represented in
        char matrix `input_matrix`.
        '''
        self.graph = self.create_graph(input_matrix)

    def create_graph(self, input_matrix):
        G = nx.Graph()

        self.rows = len(input_matrix)
        self.cols = len(input_matrix[0])

        for i in range(self.rows):
            for j in range(self.cols):
                if input_matrix[i][j] == WALL:
                    continue
                elif input_matrix[i][j] == START:
                    self.start = (i, j)
                elif input_matrix[i][j] == END:
                    self.end = (i, j)

                # else if is a valid cell
                for move in self.get_moves((i, j), input_matrix):
                    G.add_edge((i, j), move)

        return G

    def get_moves(self, coords, input_matrix):
        steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        moves = []

        for step in steps:
            move = (coords[0] + step[0], coords[1] + step[1])

            # print(move)
            if not (0 <= move[0] < self.rows and
                    0 <= move[1] < self.cols) or \
                    input_matrix[move[0]][move[1]] == WALL:
                continue

            moves.append(move)

        return moves

    def __str__(self):
        return str(self.graph.edges)
