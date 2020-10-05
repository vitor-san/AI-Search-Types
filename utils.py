import math


def euclidian_distance(coord, target):
    return math.sqrt(((coord[0] - target[0]) * (coord[0] - target[0])) +
                     ((coord[1] - target[1]) * (coord[1] - target[1])))
