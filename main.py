import sys
import os
from utils import get_graph_from_file
from metrics import get_metrics, plot_metrics


TEST_FILES = [ test for test in os.listdir('test_cases') if test[-3:] == '.in' ]
ALGORITHMS = ['dfs', 'bfs', 'best-fs', 'a-star', 'hill-climbing']

def visualize_metrics(heuristic):    
    metrics = []
    for test_file in TEST_FILES:
        g = get_graph_from_file(test_file)
        for algorithm in ALGORITHMS:
            metrics.append(get_metrics(g, algorithm, heuristic))
    plot_metrics(metrics)

def main():
    print('Qual modo deseja executar o programa?')
    print('0: Comparação das métricas para todos os casos de teste')
    print('1: Visualizar caminhos dos algoritmos para um caso de teste')
    option = int(input())

    print('Qual heurística deseja usar para as buscas informadas?')
    print('0: Distância Euclidiana')
    print('1: Distância Manhattan')
    heuristic_opt = int(input())

    heuristic = ['euclidian', 'manhattan'][heuristic_opt]

    if option == 0:
        visualize_metrics(heuristic)
    
    elif option == 1:
        print('Insira o nome do arquivo de teste:', end=' ')
        filename = input()
        get_graph_from_file(filename)
        # TODO


if __name__ == '__main__':
    main()
