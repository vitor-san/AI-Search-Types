import networkx as nx
from queue import PriorityQueue
import math

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

            if not (0 <= move[0] < self.rows and
                    0 <= move[1] < self.cols) or \
                    input_matrix[move[0]][move[1]] == WALL:
                continue

            moves.append(move)

        return moves

    def get_nodes(self):
        return self.graph.nodes

    # Get the path of the search from the parent vector
    def get_correct_path(self, parent):

        correct_path = []

        cur_coord = self.end

        while parent.get(cur_coord):
            correct_path.append(cur_coord)
            cur_coord = parent[cur_coord]

        correct_path.append(self.start)

        correct_path.reverse()

        return correct_path

    def depth_fs(self):
        stack = []
        visited = {}
        parent = {}
        complete_path = []

        visited[self.start] = True
        stack.append(self.start)

        while len(stack) > 0:
            coord = stack.pop()
            complete_path.append(coord)

            if coord == self.end:
                break

            for neighbor in self.graph[coord]:
                if neighbor not in visited:
                    parent[neighbor] = coord
                    visited[neighbor] = True
                    stack.append(neighbor)

        return self.get_correct_path(parent), complete_path

    def breadth_fs(self):
        queue = []
        visited = {}
        parent = {}
        complete_path = []

        visited[self.start] = True
        queue.append(self.start)

        while len(queue) > 0:
            coord = queue.pop(0)

            complete_path.append(coord)

            if coord == self.end:
                break

            for neighbor in self.graph[coord]:
                if neighbor not in visited:
                    parent[neighbor] = coord
                    visited[neighbor] = True
                    queue.append(neighbor)

        return self.get_correct_path(parent), complete_path

    def best_fs(self, heuristic):
        priority_queue = PriorityQueue()
        visited = {}
        parent = {}
        complete_path = []

        dist = heuristic(self.start, self.end)
        visited[self.start] = True
        priority_queue.put((dist, (self.start)))

        while not priority_queue.empty():
            _, coord = priority_queue.get()

            complete_path.append(coord)

            if coord == self.end:
                break

            for neighbor in self.graph[coord]:
                if neighbor not in visited:
                    priority_queue.put(
                        (heuristic(neighbor, self.end), neighbor))
                    parent[neighbor] = coord
                    visited[neighbor] = True

        return self.get_correct_path(parent), complete_path

    def a_star(self, heuristic):
        priority_queue = PriorityQueue()
        visited = {}
        parent = {}
        complete_path = []

        cost = 0 + heuristic(self.start, self.end)
        priority_queue.put((cost, (self.start)))
        visited[self.start] = True

        while not priority_queue.empty():
            coord_cost, coord = priority_queue.get()
            dist_to_coord = coord_cost - heuristic(coord, self.end)

            complete_path.append(coord)

            if coord == self.end:
                break

            for neighbor in self.graph[coord]:
                if neighbor not in visited:
                    priority_queue.put((1 + dist_to_coord + heuristic(neighbor, self.end),
                                        neighbor))
                    parent[neighbor] = coord
                    visited[neighbor] = True

        return self.get_correct_path(parent), complete_path

    def __str__(self):
        return str(self.graph.edges)
