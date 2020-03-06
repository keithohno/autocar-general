
import matplotlib.pyplot as plt
import numpy as np

# how much do we hate cones?
# less -> not so much, more -> we hate cones
cone_weight = 10

# turns the voronoi object thing into a weighted adjacency map
def vor_to_amap(vor):
    """Converts the voronoi data structure into a weighted adjacency map
    
    In the resulting graph data structure g, g[x][y] represents the distance
    between point x and point y, or zero if no edge exists which connects them.
    """
    # make a big 2D array of zeroes
    size = len(vor.vertices)
    graph = [[0 for x in range(size)] for y in range(size)]
    # this is a scary block of code
    #
    # in the voronoi data structure we have the following:
    # - ridge_vertices is a list of pairs of connected vertices in the Voronoi
    #   diagram. Call this an `edge`.
    # - ridge_points is a list of pairs of points in the input graph which
    #   straddle a Voronoi edge. Call this a pair of `cones`.
    # - points is a list of coordinates for the points in the input graph.
    # - vertices is a list of coordinates for the points in the Voronoi diagram.
    for edge, cones in zip(vor.ridge_vertices, vor.ridge_points):
        p1 = edge[0]
        p2 = edge[1]
        c1 = cones[0]
        c2 = cones[1]
        # discard edges that have endpoints at inifinty
        if p1 != -1 and p2 != -1:
            # generate a weight for euclidean distance
            dist_weight = distance(vor.vertices[p1], vor.vertices[p2])
            # generate a weight for obstactle (cone) proximity
            cone_weight = cone_cost(vor.points[c1], vor.points[c2])
            # put the weights into the output graph
            weight = dist_weight + cone_weight
            graph[p1][p2] = weight
            graph[p2][p1] = weight

    return graph

# euclidean distance
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# gets a list corresponding to a shortest path given by dijkstra
# p1 to p2
def get_path(path_matrix, p1, p2):
    """Turns the output of dijkstra's algorithm into a list of points to visit"""
    # path_matrix[x][y] gives the next vertex to go to when traveling from x to y.
    # -9999 indicates that we have arrived at our destination
    path = [p2]
    while path_matrix[p1][p2] != -9999:
        path.append(path_matrix[p1][p2])
        p2 = path_matrix[p1][p2]
    path.reverse()
    return path

# plots a given path with matplotlib
def plot_path(path, vertices):
    """Plots a linked line between lists of vertices"""
    for i in range(len(path) - 1):
        p1 = path[i]
        p2 = path[i+1]
        plt.plot([vertices[p1][0], vertices[p2][0]], [vertices[p1][1], vertices[p2][1]], c="green", linewidth=3.0)

# cost function for going between cones
# this can be changed
def cone_cost(p1, p2):
    dist = distance(p1, p2)
    if distance (p1, p2) <= 1:
        return 1.0 * cone_weight * (2 - dist)
    elif dist <= 2:
        return .5 * cone_weight * (2 - dist)
    return 0
