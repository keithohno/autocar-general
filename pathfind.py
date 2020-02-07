
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.sparse.csgraph import shortest_path, dijkstra

# how much do we hate cones?
# less -> not so much, more -> we hate cones
cone_weight = 10

# input set 1 (example cones)
def get_inputs_1():
    cone_points = [[2, 0], [3, 0], [-4, 2], [-2, 2], [0, 2], [-3, 1], [-1, 1], [1, 1], [3, 4], [4, 4], [-3, 5], [-4, 6], [-3, 7], [-1, 7], [0, 7], [1, 7], [2, 7], [3, 8], [0, 10], [-1, 10], [-2, 10], [-3, 10], [-4, 10]]
    left = -4.8
    right = 4.8
    min = 20000
    max = -20000
    for item in cone_points:
        if item[1] < min:
            min = item[1]
        if item[1] > max:
            max = item[1]
    bound_points = []
    for i in range(min - 2, max*2 + 2):
        bound_points.append([left, i / 2])
        bound_points.append([right, i / 2])
    cone_points.extend(bound_points)
    return np.array(cone_points)

# input set 2 (cones in an L)
def get_inputs_2():
    points = []
    for i in range(0, 20):
        points.append([-4, i / 10])
    for i in range(0, 15):
        points.append([-3, i / 10])
    for i in range(0, 20):
        points.append([-4 + i / 10, 2])
    for i in range(0, 15):
        points.append([-3 + i / 10, 1.5])
    return np.array(points)

# input set 3 (simple square thing)
def get_inputs_3():
    return np.array([[-2, 0], [2, 0], [0, -2], [0, 2], [0, 0]])

# turns the voronoi object thing into a weighted adjacency map
def vor_to_graph(vor):
    size = len(vor.vertices)
    graph = [[0 for x in range(size)] for y in range(size)]
    for edge, cones in zip(vor.ridge_vertices, vor.ridge_points):
        if edge[0] != -1 and edge[1] != -1:
            dist_weight = distance(vor.vertices[edge[0]], vor.vertices[edge[1]])
            cone_weight = cone_cost(vor.points[cones[0]], vor.points[cones[1]])
            weight = dist_weight + cone_weight
            graph[edge[0]][edge[1]] = weight
            graph[edge[1]][edge[0]] = weight
    return graph

# euclidean distance
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# gets a list corresponding to a shortest path given by dijkstra
# p1 to p2
def get_path(path_matrix, p1, p2):
    path = [p2]
    while path_matrix[p1][p2] != -9999:
        path.append(path_matrix[p1][p2])
        p2 = path_matrix[p1][p2]
    path.reverse()
    return path

# plots a given path with matplotlib
def plot_path(path, vertices):
    for i in range(len(path) - 1):
        p1 = path[i]
        p2 = path[i+1]
        plt.plot([vertices[p1][0], vertices[p2][0]], [vertices[p1][1], vertices[p2][1]], c="green", linewidth=3.0)

# cost function for going between cones
def cone_cost(p1, p2):
    dist = distance(p1, p2)
    if distance (p1, p2) <= 1:
        return 1.0 * cone_weight * (2 - dist)
    elif dist <= 2:
        return .5 * cone_weight * (2 - dist)
    return 0

points = get_inputs_1()

vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.axis('scaled')
plt.ylim((-2,14))
plt.xlim((-6,6))

graph = vor_to_graph(vor)
(dist_matrix, path_matrix) = dijkstra(graph, return_predecessors=True)
# print(vor.vertices)
# print(graph)
# print(dist_matrix)
# print(path_matrix)

# get point with lowest and highest y-value
low_p = 0
high_p = 0
min_y = 20000
max_y = -20000
for i in range(len(vor.vertices)):
    if vor.vertices[i][1] < min_y:
        low_p = i
        min_y = vor.vertices[i][1]
    if vor.vertices[i][1] > max_y:
        high_p = i
        max_y = vor.vertices[i][1]

path = get_path(path_matrix, high_p, low_p)
# print(path)
plot_path(path, vor.vertices)

plt.show()