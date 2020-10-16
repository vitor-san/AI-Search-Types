from heuristics import euclidian_distance, manhattan_distance 

import matplotlib.pyplot as plt
import time


N_REPETITIONS = 10      # How many times to run timing experiment

def get_time(f, *args, **kwargs):
    a = time.time()
    ret = f(*args, **kwargs)
    b = time.time()
    return b - a, ret


def plot_metrics(metrics, test_case, heuristic):

    Ns = []
    algorithm_names = [ metric['algorithm'] for metric in metrics ]
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

    fig.suptitle(f'Comparação de métricas dos algoritmos para o caso de teste {test_case} com heurística {heuristic}')

    # Configuring execution time data
    time_ax.set_title(f'Tempo médio de {metrics[0]["n_repetitions"]} execuções por algoritmo')
    time_ax.set_ylabel('Média de tempo (s)')
    time_ax.set_xticks(range(len(algorithm_names)))
    time_ax.set_xticklabels(algorithm_names)
    time_ax.set_ylim(**(get_ylims(times, found_goal)))
    time_ax.bar(range(len(algorithm_names)), times, color=found_goal)

    # Configuring path length data
    len_ax.set_title('Tamanho do caminho encontrado por algoritmo')
    len_ax.set_ylabel('Tamanho do caminho')
    len_ax.set_xticks(range(len(algorithm_names)))
    len_ax.set_xticklabels(algorithm_names)
    len_ax.set_ylim(**(get_ylims(path_len, found_goal)))
    len_ax.bar(range(len(algorithm_names)), path_len, color=found_goal)

    # Configuring efficiency data
    eff_ax.set_title('Eficiência por algoritmo')
    eff_ax.set_ylabel('Eficiência')
    eff_ax.set_xticks(range(len(algorithm_names)))
    eff_ax.set_xticklabels(algorithm_names)
    eff_ax.set_ylim(**(get_ylims(efficiency, found_goal)))
    eff_ax.bar(range(len(algorithm_names)), efficiency, color=found_goal)

    # Configuring speed data
    speed_ax.set_title('Média de nós visitados por segundo por algoritmo')
    speed_ax.set_ylabel('Nós por segundo')
    speed_ax.set_xticks(range(len(algorithm_names)))
    speed_ax.set_xticklabels(algorithm_names)
    speed_ax.set_ylim(**(get_ylims(speed, found_goal)))
    speed_ax.bar(range(len(algorithm_names)), speed, color=found_goal)

    # Configuring backtracking data (TODO)
    bt_ax.set_title('Número de backtracks por algoritmo')
    bt_ax.set_ylabel('Backtracks')
    bt_ax.set_xticks(range(len(algorithm_names)))
    bt_ax.set_xticklabels(algorithm_names)
    # bt_ax.set_ylim(**(get_ylims(backtracks, found_goal)))
    # eff_ax.bar(range(len(algorithm_names)), backtracks, color=found_goal)

    plt.tight_layout()
    plt.show()


# Ignore data from algorithm in y limits if path wasn't found
def get_ylims(data, found):    
    max_y, min_y = data[0], data[0]

    for num, was_found in zip(data, found):
        if was_found == 'g':
            max_y = max(max_y, num)
            min_y = min(min_y, num)

    return {
        'bottom': min_y*0.95,
        'top': max_y*1.05
    }


def get_metrics(g, heuristic_name, n_repetitions=N_REPETITIONS):

    heuristic, path, visited, time = None, None, None, None

    if heuristic_name == 'euclidian':
        heuristic = euclidian_distance

    elif heuristic_name == 'manhattan':
        heuristic = manhattan_distance

    algorithms = [g.breadth_fs, g.depth_fs, g.best_fs, g.a_star, g.hill_climbing]
    algorithm_names = ['BFS', 'DFS', 'BeFS', 'A*', 'HC']
    args = [[], [], [heuristic], [heuristic], [heuristic]]

    metrics = []

    for arg, algorithm, algorithm_name in zip(args, algorithms, algorithm_names):
        time, (path, visited) = get_time(algorithm, *arg)
        for i in range(n_repetitions - 1):
            time += get_time(algorithm, *arg)[0]
        time /= n_repetitions

        metrics.append({
            'algorithm': algorithm_name,
            'n_repetitions': n_repetitions,
            'n_vertices': len(g.nodes),
            'n_edges': len(g.edges),
            'avg_time': time,
            'backtracks': None,  # Número de backtracks parece ter que ser instrumentado na implementação
            'path_len': len(path),
            'found_goal': path[-1] == g.end,
            'efficiency': len(path)/len(visited),
            'speed': len(g.nodes)/(time + 1e-12) # Adding 10^-12 to prevent division by zero on fast executions
        })

    return metrics