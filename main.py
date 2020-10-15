import sys
from utils import visualize_path, get_graph_from_file
from heuristic import euclidian_distance, manhattan_distance


def main():
    g = get_graph_from_file(sys.argv[1])
    path_to_goal, visited = g.a_star(manhattan_distance)
    visualize_path(g, path_to_goal, visited)


if __name__ == '__main__':
    main()
