import sys
from matplotlib import pyplot as plt, transforms, animation
from graph import Graph
from custom_plots import MyScatter
from utils import euclidian_distance



def visualize_path(g):
    path_to_goal, visited = g.depth_fs()

    # We don't want the start and end nodes to be in the path (because of ploting),
    # so let's remove them from it.
    path_to_goal = path_to_goal[1:-1]
    visited = visited[1:-1]

    # Now, we will plot all of the points, coloring them appropriately

    figure, axes = plt.subplots(dpi=141)

    axes.set_xlim(-0.5, g.cols - 0.5)
    axes.set_ylim(-0.5, g.rows - 0.5)

    axes.xaxis.set_ticks([])  # remove ticks
    axes.yaxis.set_ticks([])  # remove ticks

    axes.set_ylim(axes.get_ylim()[::-1])        # invert the y-axis
    axes.xaxis.tick_top()                     # and move the x-axis
    axes.yaxis.tick_left()  # remove right y-ticks

    g_nodes = g.get_nodes()

    x = []
    y = []

    color = []
    marker = []

    axes.set_aspect('equal')
    line, = axes.plot([], [], lw=3)

    def init():
        return line,

    def animate(step):
        was_defined = False
        scatter = None

        if step == 0:
            for i in range(g.rows):
                for j in range(g.cols):
                    x.append(j)
                    y.append(i)
                    if (i, j) not in g_nodes:
                        # It's an obstacle!!
                        color.append("black")
                        marker.append("s")
                    elif (i, j) == g.start:
                        color.append("green")
                        marker.append("h")
                    elif (i, j) == g.end:
                        color.append("red")
                        marker.append("X")
                    else:
                        color.append("white")
                        marker.append("s")
        else:
            for xi, yi in visited[:step]:  # all points up to this step
                index = xi * g.cols + yi
                if (xi, yi) in path_to_goal:
                    color[index] = "navy"
                    marker[index] = "o"
                else:
                    color[index] = "dimgray"
                    marker[index] = "o"

        if not was_defined:
            scatter = MyScatter(x, y, axes, markers=marker,
                                colors=color, linewidth=0)
        else:
            scatter.update(marker, color)

        return line,

    # call the animator
    anim = animation.FuncAnimation(figure, animate, frames=len(
        visited) + 2, init_func=init, interval=100, blit=True, repeat=False)

    plt.show()


def main():
    with open(sys.argv[1]) as f:
        dimensions_s = f.readline().split()
        dimensions = (int(dimensions_s[0]), int(dimensions_s[1]))

        matrix = []

        for line in f.readlines():
            matrix.append(list(line.strip()))

        g = Graph(matrix)
        visualize_path(g)


if __name__ == '__main__':
    main()