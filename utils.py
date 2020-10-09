import math


def euclidian_distance(coord, target):
    return math.sqrt(sum([(coord[i] - target[i])**2 for i in range(len(coord))]))


def manhattan_distance(coord, target):
    return sum([math.fabs(coord[i] - target[i]) for i in range(len(coord))])