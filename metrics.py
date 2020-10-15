from heuristics import euclidian_distance, manhattan_distance 

import matplotlib.pyplot as plt
import time


N_REPETITIONS = 10      # How many times to run timing experiment

def get_time(f, *args, **kwargs):
    a = time.time()
    ret = f(*args, **kwargs)
    b = time.time()
    return b - a, ret


def plot_metrics(metrics, algorithm=None):

    Ns = []
    test_cases = [ f'{i+1}.in' for i in range(len(metrics)) ]
    times = []
    path_len = []
    found_goal = []
    efficiency = []
    speed = []

    for metric in metrics:
        Ns.append((metric['n_vertices'], metric['n_edges']))
        times.append(metric['avg_time'])
        path_len.append(metric['path_len'])
        found_goal.append('g' if metric['found_goal'] else 'r') # Setting red/green color if found
        efficiency.append(metric['efficiency'])
        speed.append(metric['speed'])

    fig, ((_,_), (len_ax, eff_ax), (speed_ax, bt_ax)) = plt.subplots(3, 2)   # Creating 3x2 grid
    time_ax = plt.subplot(3, 1, 1)  # Selecting first row as a single plot (execution time)

    if algorithm is not None:
        fig.suptitle(f'Métricas coletadas para o algoritmo {algorithm}')

    # Configuring execution time data
    time_ax.set_title(f'Tempo médio de {metrics[0]["n_repetitions"]} execuções por caso de teste')
    time_ax.set_xlabel('Caso de teste')
    time_ax.set_ylabel('Média de tempo (s)')
    time_ax.set_xticks(range(len(test_cases)))
    time_ax.set_xticklabels(test_cases)
    time_ax.bar(range(len(test_cases)), times, color=found_goal)

    # Configuring path length data
    len_ax.set_title('Tamanho do caminho encontrado por caso de teste')
    len_ax.set_xlabel('Caso de teste')
    len_ax.set_ylabel('Tamanho do caminho')
    len_ax.set_xticks(range(len(test_cases)))
    len_ax.set_xticklabels(test_cases)
    len_ax.bar(range(len(test_cases)), path_len, color=found_goal)

    # Configuring efficiency data
    eff_ax.set_title('Eficiência por caso de teste')
    eff_ax.set_xlabel('Caso de teste')
    eff_ax.set_ylabel('Eficiência')
    eff_ax.set_xticks(range(len(test_cases)))
    eff_ax.set_xticklabels(test_cases)
    eff_ax.bar(range(len(test_cases)), efficiency, color=found_goal)

    # Configuring speed data
    speed_ax.set_title('Média de nós visitados por segundo por caso de teste')
    speed_ax.set_xlabel('Caso de teste')
    speed_ax.set_ylabel('Nós por segundo')
    speed_ax.set_xticks(range(len(test_cases)))
    speed_ax.set_xticklabels(test_cases)
    speed_ax.bar(range(len(test_cases)), speed, color=found_goal)

    # Configuring backtracking data (TODO)
    bt_ax.set_title('Número de backtracks por caso de teste')
    bt_ax.set_xlabel('Caso de teste')
    bt_ax.set_ylabel('Backtracks')
    bt_ax.set_xticks(range(len(test_cases)))
    bt_ax.set_xticklabels(test_cases)
    # eff_ax.bar(range(len(test_cases)), speed, color=found_goal)

    plt.tight_layout()
    plt.show()


def get_metrics(g, algorithm_name, heuristic_name, n_repetitions=N_REPETITIONS):

    heuristic, path, visited, time = None, None, None, None

    if heuristic_name == 'euclidian':
        heuristic = euclidian_distance

    elif heuristic_name == 'manhattan':
        heuristic = manhattan_distance

    if algorithm_name == 'bfs':
        time, (path, visited) = get_time(g.breadth_fs)
        for i in range(n_repetitions - 1):
            time += get_time(g.breadth_fs)[0]
        time /= n_repetitions

    elif algorithm_name == 'dfs':
        time, (path, visited) = get_time(g.depth_fs)
        for i in range(n_repetitions - 1):
            time += get_time(g.depth_fs)[0]
        time /= n_repetitions

    elif algorithm_name == 'best-first':
        time, (path, visited) = get_time(g.best_fs, heuristic)
        for i in range(n_repetitions - 1):
            time += get_time(g.best_fs, heuristic)[0]
        time /= n_repetitions

    elif algorithm_name == 'a-star':
        time, (path, visited) = get_time(g.a_star, heuristic)
        for i in range(n_repetitions - 1):
            time += get_time(g.a_star, heuristic)[0]
        time /= n_repetitions

    elif algorithm_name == 'hill-climbing':
        time, (path, visited) = get_time(g.hill_climbing, heuristic)
        for i in range(n_repetitions - 1):
            time += get_time(g.hill_climbing, heuristic)[0]
        time /= n_repetitions

    return {
        'n_repetitions': n_repetitions,
        'n_vertices': len(g.nodes),
        'n_edges': len(g.edges),
        'avg_time': time,
        'backtracks': None,  # Número de backtracks parece ter que ser instrumentado na implementação
        'path_len': len(path),
        'found_goal': path[-1] == g.end,
        'efficiency': len(path)/len(visited),
        'speed': len(g.nodes)/(time + 1e-12) # Adding 10^-12 to prevent division by zero on fast executions
    }