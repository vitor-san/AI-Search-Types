from graph import Graph
import sys

with open(sys.argv[1]) as f:
    dimensions_s = f.readline().split()
    dimensions = (int(dimensions_s[0]), int(dimensions_s[1]))

    matrix = []

    for line in f.readlines():
        matrix.append(list(line.strip()))

    g = Graph(matrix)
    print(g)
