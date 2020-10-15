from heuristics import euclidian_distance, manhattan_distance 

import matplotlib.pyplot as plt
import time


N_REPETITIONS = 10      # How many times to run timing experiment

def get_time(f, *args, **kwargs):
    a = time.time()
    ret = f(*args, **kwargs)
    b = time.time()
    return b - a, ret


def plot_metrics(metrics):
    pass


def get_metrics(g, algorithm_name, heuristic_name):

    heuristic, path, visited, time = None, None, None, None

    if heuristic_name == 'euclidian':
        heuristic = euclidian_distance

    elif heuristic_name == 'manhattan':
        heuristic = manhattan_distance

    if algorithm_name == 'bfs':
        time, (path, visited) = get_time(g.breadth_fs)
        for i in range(N_REPETITIONS - 1):
            time += get_time(g.breadth_fs)[0]
        time /= N_REPETITIONS

    elif algorithm_name == 'dfs':
        time, (path, visited) = get_time(g.depth_fs)
        for i in range(N_REPETITIONS - 1):
            time += get_time(g.depth_fs)[0]
        time /= N_REPETITIONS

    elif algorithm_name == 'best-first':
        time, (path, visited) = get_time(g.best_fs, heuristic)
        for i in range(N_REPETITIONS - 1):
            time += get_time(g.best_fs, heuristic)[0]
        time /= N_REPETITIONS

    elif algorithm_name == 'a-star':
        time, (path, visited) = get_time(g.a_star, heuristic)
        for i in range(N_REPETITIONS - 1):
            time += get_time(g.a_star, heuristic)[0]
        time /= N_REPETITIONS

    elif algorithm_name == 'hill-climbing':
        time, (path, visited) = get_time(g.hill_climbing, heuristic)
        for i in range(N_REPETITIONS - 1):
            time += get_time(g.hill_climbing, heuristic)[0]
        time /= N_REPETITIONS

    return {
        'avg_time': time,
        'backtracks': None,  # Número de backtracks parece ter que ser instrumentado na implementação
        'path_len': len(path),
        'found_goal': path[0] == g.start,
        'efficiency': len(path)/len(visited),
        'speed': len(g.edges)/time
    }