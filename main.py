import sys
import os
from utils import get_graph_from_file
from metrics import get_metrics, plot_metrics


TEST_FILES = [ os.path.join('test_cases', test) for test in os.listdir('test_cases') if test[-3:] == '.in' ]
ALGORITHMS = ['dfs', 'bfs', 'best-fs', 'a-star', 'hill-climbing']

def visualize_metrics(algorithm, heuristic):
    metrics = []
    for test_file in TEST_FILES:
        g = get_graph_from_file(test_file)
        metrics.append(get_metrics(g, algorithm, heuristic))
    
    plot_metrics(metrics, algorithm)


def main():
    print('Em qual modo deseja executar o programa?')
    print('0: Visualizar as métricas de um algoritmo para todos os casos de teste')
    print('1: Visualizar caminhos dos algoritmos para um caso de teste')
    option = int(input())

    print('Qual heurística deseja usar para as buscas informadas?')
    print('0: Distância Euclidiana')
    print('1: Distância Manhattan')
    heuristic_opt = int(input())

    heuristic = ['euclidian', 'manhattan'][heuristic_opt]

    if option == 0:
        print('Qual algoritmo?')
        print('0: DFS')
        print('1: BFS')
        print('2: Best-first search')
        print('3: A*')
        print('4: Hill climbing')

        algorithm_opt = int(input())
        algorithm = ALGORITHMS[algorithm_opt]
        visualize_metrics(algorithm, heuristic)
    
    elif option == 1:
        print('Insira o nome do arquivo de teste:', end=' ')
        filename = input()
        get_graph_from_file(filename)
        # TODO


if __name__ == '__main__':
    visualize_metrics('hill-climbing', 'manhattan')
