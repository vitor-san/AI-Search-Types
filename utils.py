import sys
from matplotlib import pyplot as plt, transforms, animation
from graph import Graph


def get_graph_from_file(filename):
    with open(filename) as f:
        matrix = []
        for line in f.readlines()[1:]:
            matrix.append(list(line.strip()))
        g = Graph(matrix)
        return g


def visualize_path(g, paths):
    figure, axs = plt.subplots(nrows=2, ncols=5, dpi=141, figsize=(15, 15))

    for i, (goal_nodes, visited_nodes) in enumerate(paths):
        # Exclude the starting point
        visited_nodes = visited_nodes[1:]

        # Now, we will plot all of the points, coloring them appropriately
        ax = axs[0][i]

        # Prepare the axes
        # ---------
        ax.set_xlim(-0.5, g.cols - 0.5)
        ax.set_ylim(-0.5, g.rows - 0.5)

        ax.xaxis.set_ticks([])  # remove ticks
        ax.yaxis.set_ticks([])  # remove ticks

        ax.set_ylim(ax.get_ylim()[::-1])        # invert the y-axis
        ax.xaxis.tick_top()                     # and move the x-axis
        ax.yaxis.tick_left()  # remove right y-ticks

        ax.set_aspect('equal')
        line, = ax.plot([], [])
        # ---------

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
                    color.append("green")
                    marker.append("h")
                    continue

                if (i, j) == g.end:
                    color.append("red")
                    marker.append("X")
                    continue

                if (i, j) in goal_nodes:
                    color.append("navy")
                    marker.append("o")
                elif (i, j) in visited_nodes:
                    color.append("dimgray")
                    marker.append("o")
                else:
                    color.append("white")
                    marker.append("s")

        MyScatter(x, y, ax, markers=marker, colors=color, linewidth=0)

    plt.show()
