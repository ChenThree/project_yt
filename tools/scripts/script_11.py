import numpy as np

from tools.utils.plot_helpers import plot_user_degree_KMeans_graph

def script_11(project):
    # get degrees
    user_count = project.get_user_count()
    in_degrees, out_degrees = project.get_degrees()
    # convert to [in_degree, out_degree]
    pos = np.zeros((user_count, 2))
    for i, (in_degree, out_degree) in enumerate(zip(in_degrees.values(), out_degrees.values())):
        pos[i, 0] = in_degree
        pos[i, 1] = out_degree
    # print(pos)
    # plot Kmeans
    plot_user_degree_KMeans_graph(pos)