import sys
import os
from utils import get_graph_from_file
from metrics import get_metrics, plot_metrics


TEST_FILES = sorted([os.path.join('test_cases', test)
                     for test in os.listdir('test_cases') if test[-3:] == '.in'])


def visualize_metrics(test_case, heuristic, mode):
    g = get_graph_from_file(test_case)
    metrics = get_metrics(g, heuristic)
    plot_metrics(metrics, os.path.split(test_case)[1], heuristic, mode)


def main():
    print('Qual heurística deseja usar para as buscas informadas? (padrão = 1)\nPressione ENTER para escolher o padrão.\n')
    print('0: Distância Euclidiana')
    print('1: Distância Manhattan')
    print('2: Média entre euclidiana e manhattan')

    inp = input()
    inp = 1 if inp == '' else inp
    heuristic_opt = int(inp)

    heuristic = ['euclidian', 'manhattan', 'average'][heuristic_opt]

    print('\nQual caso de teste? (padrão = 4)\nPressione ENTER para escolher o padrão.\n')
    for i, test in enumerate(TEST_FILES):
        print(f'{i+1}: {os.path.split(test)[1]}')

    inp = input()
    inp = 4 if inp == '' else inp
    file = int(inp)

    print('\nVocê quer ver as métricas de distância até o objetivo ou velocidade e número de backtracks? (padrão = 1)\nPressione ENTER para escolher o padrão.\n')
    print('0: Distância até o objetivo')
    print('1: Velocidade e número de backtracks')

    inp = input()
    inp = 1 if inp == '' else inp
    mode = int(inp)

    visualize_metrics(TEST_FILES[file-1], heuristic, mode)


if __name__ == '__main__':
    main()
