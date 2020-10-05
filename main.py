from graph import Graph
import sys
from matplotlib import pyplot as plt, transforms
from custom_plots import mscatter
from utils import euclidian_distance

with open(sys.argv[1]) as f:
    dimensions_s = f.readline().split()
    dimensions = (int(dimensions_s[0]), int(dimensions_s[1]))

    matrix = []

    for line in f.readlines():
        matrix.append(list(line.strip()))

    g = Graph(matrix)
    path_to_goal, visited = g.depth_fs()

    # We will plot all of the points, coloring them appropriately

    # first of all, the base transformation of the data points is needed
    base = plt.gca().transData
    rot = transforms.Affine2D().rotate_deg(-90)

    g_nodes = g.get_nodes()

    x = []
    y = []

    color = []
    marker = []

    for i in range(g.rows):
        for j in range(g.cols):
            x.append(i)
            y.append(j)

            if (i, j) not in g_nodes:
                # It's an obstacle!!
                color.append("black")
                marker.append("s")
                continue

            if (i, j) == g.start:
                color.append("navy")
                marker.append("s")
                continue

            if (i, j) == g.end:
                color.append("green")
                marker.append("s")
                continue

            if (i, j) in path_to_goal:
                color.append("orangered")
                marker.append("o")
            elif (i, j) in visited:
                color.append("dimgray")
                marker.append("o")
            else:
                color.append("white")
                marker.append("s")

    mscatter(x, y, color=color, m=marker, transform=rot + base)
    plt.axis('equal')

    plt.show()
