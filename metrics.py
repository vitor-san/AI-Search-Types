from heuristics import euclidian_distance, manhattan_distance, mean_manh_eucli

import matplotlib.pyplot as plt
import time


N_REPETITIONS = 10      # How many times to run timing experiment


def get_time(f, *args, **kwargs):
    a = time.time()
    ret = f(*args, **kwargs)
    b = time.time()
    return b - a, ret


def plot_metrics(metrics, test_case, heuristic, mode):

    Ns = []
    algorithm_names = [metric['algorithm'] for metric in metrics]
    times = []
    path_len = []
    found_goal = []
    efficiency = []
    backtracks = []
    speed = []
    images = []
    distances = []

    for metric in metrics:
        Ns.append((metric['n_vertices'], metric['n_edges']))
        times.append(1000*metric['avg_time'])
        path_len.append(metric['path_len'])
        backtracks.append(metric['backtracks'])
        # Setting red/green color if found
        found_goal.append('g' if metric['found_goal'] else 'r')
        efficiency.append(metric['efficiency'])
        speed.append(metric['speed'])
        images.append(metric['image'])
        distances.append(metric['dist_to_goal'])

    fig, len_ax, eff_ax, speed_ax, bt_ax, time_ax = None, None, None, None, None, None

    if mode == 0:
        fig, axs = plt.subplots(2, 5)   # Creating 2x5 grid

        # Displaying map images
        for i, (image, algorithm_name) in enumerate(zip(images, algorithm_names)):
            # Selecting the i-th subplot on the first row of a 4x5 grid
            image_ax = plt.subplot(2, 5, i + 1)
            image_ax.set_title(algorithm_name)
            image_ax.set_yticks([])
            image_ax.set_xticks([])
            image_ax.imshow(image, interpolation='nearest')

        max_dist = max([max(dist) for dist in distances])

        # Displaying distance to goal
        for i, dist in enumerate(distances):
            dist_ax = plt.subplot(2, 5, 5 + i + 1)
            dist_ax.plot(dist)
            dist_ax.set_xlabel('Iteração')
            dist_ax.set_ylim(bottom=0, top=max_dist)
            if i == 0:
                dist_ax.set_ylabel('Heurística até o objetivo')

        fig.suptitle(
            f'Comparação de desempenho dos algoritmos para o caso de teste {test_case} com heurística {heuristic}')

        plt.subplots_adjust(left=0.055, right=0.98, top=0.96, hspace=0)
        plt.show()
        return

    if mode == 1:
        fig, ((_, _), (_, _), (len_ax, eff_ax), (speed_ax, bt_ax)
              ) = plt.subplots(4, 2)   # Creating 4x2 grid
        # Selecting second row of a 4x1 as a single plot (execution time)
        time_ax = plt.subplot(4, 1, 2)

        fig.suptitle(
            f'Comparação de métricas dos algoritmos para o caso de teste {test_case} com heurística {heuristic}')

        # Configuring speed data
        speed_ax.set_title('"Velocidade" do algoritmo (nós/segundo)')
        speed_ax.set_xticks(range(len(algorithm_names)))
        speed_ax.set_xticklabels(algorithm_names)
        speed_ax.set_ylim(**(get_ylims(speed, found_goal)))
        speed_ax.bar(range(len(algorithm_names)), speed, color=found_goal)

        # Configuring backtracking data
        bt_ax.set_title('Número de backtracks do algoritmo')
        bt_ax.set_xticks(range(len(algorithm_names)))
        bt_ax.set_xticklabels(algorithm_names)
        bt_ax.set_ylim(**(get_ylims(backtracks, found_goal)))
        bt_ax.bar(range(len(algorithm_names)), backtracks, color=found_goal)

        # Displaying map images
        for i, (image, algorithm_name) in enumerate(zip(images, algorithm_names)):
            # Selecting the i-th subplot on the first row of a 4x5 grid
            image_ax = plt.subplot(4, 5, i + 1)
            image_ax.set_title(algorithm_name)
            image_ax.set_yticks([])
            image_ax.set_xticks([])
            image_ax.imshow(image, interpolation='nearest')

        # Configuring execution time data
        time_ax.set_title(
            f'Tempo médio de {metrics[0]["n_repetitions"]} execuções do algoritmo (em milissegundos)')
        time_ax.set_xticks(range(len(algorithm_names)))
        time_ax.set_xticklabels(algorithm_names)
        time_ax.set_ylim(**(get_ylims(times, found_goal)))
        time_ax.bar(range(len(algorithm_names)), times, color=found_goal)

        # Configuring path length data
        len_ax.set_title('Tamanho do caminho encontrado pelo algoritmo')
        len_ax.set_xticks(range(len(algorithm_names)))
        len_ax.set_xticklabels(algorithm_names)
        len_ax.set_ylim(**(get_ylims(path_len, found_goal)))
        len_ax.bar(range(len(algorithm_names)), path_len, color=found_goal)

        # Configuring efficiency data
        eff_ax.set_title('Eficiência do algoritmo')
        eff_ax.set_xticks(range(len(algorithm_names)))
        eff_ax.set_xticklabels(algorithm_names)
        eff_ax.bar(range(len(algorithm_names)), efficiency, color=found_goal)

        plt.subplots_adjust(left=0.06, bottom=0.06,
                            hspace=0.638, right=0.967, wspace=0.31)
        plt.show()
        return


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

    elif heuristic_name == 'average':
        heuristic = mean_manh_eucli

    algorithms = [g.breadth_fs, g.depth_fs,
                  g.best_fs, g.a_star, g.hill_climbing]
    algorithm_names = ['BFS', 'DFS', 'BeFS', 'A*', 'HC']
    args = [[], [], [heuristic], [heuristic], [heuristic]]

    metrics = []

    for arg, algorithm, algorithm_name in zip(args, algorithms, algorithm_names):
        time, (path, visited, backtracks) = get_time(algorithm, *arg)
        for i in range(n_repetitions - 1):
            time += get_time(algorithm, *arg)[0]
        time /= n_repetitions

        dist_to_goal = [heuristic(coord, g.end) for coord in visited]

        metrics.append({
            'algorithm': algorithm_name,
            'n_repetitions': n_repetitions,
            'n_vertices': len(g.nodes),
            'n_edges': len(g.edges),
            'avg_time': time,
            'backtracks': backtracks,
            'path_len': len(path),
            'found_goal': path[-1] == g.end,
            'efficiency': len(path)/len(visited),
            'dist_to_goal': dist_to_goal,
            # Adding 10^-12 to prevent division by zero on fast executions
            'speed': len(g.nodes)/(time + 1e-12),
            'image': get_image(g, visited, path)
        })

    return metrics


def get_image(g, visited, path):
    image = [[(0, 0, 0)] * g.cols for i in range(g.rows)]

    for coord in g.graph.nodes:
        image[coord[0]][coord[1]] = (255, 255, 255)

    for coord in visited:
        image[coord[0]][coord[1]] = (150, 150, 150)

    for coord in path:
        image[coord[0]][coord[1]] = (255, 204, 0)

    image[g.start[0]][g.start[1]] = (51, 204, 51)
    image[g.end[0]][g.end[1]] = (204, 0, 0)

    return image
