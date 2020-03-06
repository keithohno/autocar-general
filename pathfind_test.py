
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.sparse.csgraph import shortest_path, dijkstra

from pathfind import *

def test_inputs():
    """Generates an example test input set (cones in a lane)"""
    # points are listed as an array of [x, y] pairs
    cone_points = [[2, 0], [3, 0], [-4, 2], [-2, 2], [0, 2], [-3, 1], [-1, 1], [1, 1], [3, 4], [4, 4], [-3, 5], [-4, 6], [-3, 7], [-1, 7], [0, 7], [1, 7], [2, 7], [3, 8], [0, 10], [-1, 10], [-2, 10], [-3, 10], [-4, 10]]
    # distances from left and right lane boundaries
    left = -4.8
    right = 4.8
    return process_inputs(cone_points, left, right)

def process_inputs(cone_points, left, right):
    """Processes parameters for lane position and obstacles to generate a general
    list of points to avoid"""
    # find range of y-values
    min = cone_points[0][1]
    max = cone_points[0][1]
    for item in cone_points:
        if item[1] < min:
            min = item[1]
        if item[1] > max:
            max = item[1]
    # generate points along the lane boundaries from min to max
    bound_points = []
    for i in range(min - 2, max*2 + 2):
        bound_points.append([left, i / 2])
        bound_points.append([right, i / 2])
    cone_points.extend(bound_points)
    return np.array(cone_points)

def main():
    # get inputs
    points = test_inputs()

    # generate voronoi diagram
    vor = Voronoi(points)
    # plot voronoi diagram
    fig = voronoi_plot_2d(vor)
    plt.axis('scaled')
    plt.ylim((-2,14))
    plt.xlim((-6,6))

    # convert from voronoi data structure to adjacency map
    graph = vor_to_amap(vor)
    # run dijkstra's algorithm to find the fastest way through the map
    (_, path_matrix) = dijkstra(graph, return_predecessors=True)

    # get point with lowest and highest y-value
    low_p = 0
    high_p = 0
    min_y = vor.vertices[0][1]
    max_y = vor.vertices[0][1]
    for i in range(len(vor.vertices)):
        if vor.vertices[i][1] < min_y:
            low_p = i
            min_y = vor.vertices[i][1]
        if vor.vertices[i][1] > max_y:
            high_p = i
            max_y = vor.vertices[i][1]

    # generate an actual path from dijkstra's output
    path = get_path(path_matrix, high_p, low_p)
    # plot the path
    plot_path(path, vor.vertices)

    plt.show()

if __name__ == '__main__':
    main()