import sys
from utils import visualize_path, get_graph_from_file
from heuristics import euclidian_distance, manhattan_distance


def get_h_function(name):
    if name == 'manhattan':
        return manhattan_distance
    elif name == 'euclidian':
        return euclidian_distance


def main():
    g = get_graph_from_file(sys.argv[1])

    h_name = 'manhattan'

    paths = []

    goal_nodes, visited_nodes = g.depth_fs()
    paths.append([goal_nodes, visited_nodes])

    goal_nodes, visited_nodes = g.breadth_fs()
    paths.append([goal_nodes, visited_nodes])

    goal_nodes, visited_nodes = g.best_fs(get_h_function(h_name))
    paths.append([goal_nodes, visited_nodes])

    goal_nodes, visited_nodes = g.a_star(get_h_function(h_name))
    paths.append([goal_nodes, visited_nodes])

    goal_nodes, visited_nodes = g.a_star(get_h_function(h_name))
    paths.append([goal_nodes, visited_nodes])

    visualize_path(g, paths)


if __name__ == '__main__':
    main()
