from graph import Graph
import sys
from matplotlib import pyplot as plt, transforms
from custom_plots import MyScatter
from utils import euclidian_distance

with open(sys.argv[1]) as f:
    dimensions_s = f.readline().split()
    dimensions = (int(dimensions_s[0]), int(dimensions_s[1]))

    matrix = []

    for line in f.readlines():
        matrix.append(list(line.strip()))

    g = Graph(matrix)
    path_to_goal, visited = g.depth_fs()

    # Now, we will plot all of the points, coloring them appropriately

    figure, axes = plt.subplots(dpi=141)

    delimiter_color = "black"
    delimiters_on = False

    if delimiters_on:
        # Row delimiters
        for i in range(g.rows):
            axes.axhline(i - 0.5, color=delimiter_color)
            axes.axhline(i + 0.5, color=delimiter_color)

        # Column delimiters
        for j in range(g.cols):
            axes.axvline(j - 0.5, color=delimiter_color)
            axes.axvline(j + 0.5, color=delimiter_color)

    axes.set_xlim(-0.5, g.cols - 0.5)
    axes.set_ylim(-0.5, g.rows - 0.5)

    axes.yaxis.set_ticks([])  # remove ticks
    axes.xaxis.set_ticks([])  # remove ticks

    axes.set_ylim(axes.get_ylim()[::-1])        # invert the axis
    axes.xaxis.tick_top()                     # and move the X-Axis
    axes.yaxis.tick_left()                    # remove right y-Ticks

    g_nodes = g.get_nodes()

    x = []
    y = []

    color = []
    marker = []

    use_tiny_circle = False

    for i in range(g.rows):
        for j in range(g.cols):
            x.append(j)
            y.append(i)

            if (i, j) not in g_nodes:
                # It's an obstacle!!
                color.append("black")
                marker.append("s")
                continue

            if (i, j) == g.start:
                color.append("green")
                marker.append("h")
                continue

            if (i, j) == g.end:
                color.append("red")
                marker.append("X")
                continue

            if (i, j) in path_to_goal:
                color.append("navy")
                marker.append(".") if use_tiny_circle else marker.append("o")
            elif (i, j) in visited:
                color.append("dimgray")
                marker.append(".") if use_tiny_circle else marker.append("o")
            else:
                color.append("white")
                marker.append("s")

    MyScatter(x, y, axes, m=marker, color=color, linewidth=0)
    axes.set_aspect('equal')

    plt.show()
