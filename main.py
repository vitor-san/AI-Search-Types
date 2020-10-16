import sys
import os
from utils import get_graph_from_file
from metrics import get_metrics, plot_metrics


TEST_FILES = [ os.path.join('test_cases', test) for test in os.listdir('test_cases') if test[-3:] == '.in' ]
ALGORITHMS = ['dfs', 'bfs', 'best-fs', 'a-star', 'hill-climbing']

def visualize_metrics(test_case, heuristic):
    g = get_graph_from_file(test_case)
    metrics = get_metrics(g, heuristic)    
    plot_metrics(metrics, os.path.split(test_case)[1], heuristic)


def main():
    print('Qual heurística deseja usar para as buscas informadas?')
    print('0: Distância Euclidiana')
    print('1: Distância Manhattan')
    heuristic_opt = int(input())

    heuristic = ['euclidian', 'manhattan'][heuristic_opt]

    print('Qual caso de teste?')
    for i, test in enumerate(TEST_FILES):
        print(f'{i+1}: {os.path.split(test)[1]}')
    file = int(input())

    visualize_metrics(TEST_FILES[file-1], heuristic)


if __name__ == '__main__':
    main()
