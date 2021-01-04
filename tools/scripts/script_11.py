import numpy as np

from tools.utils.plot_helpers import plot_user_degree_KMeans_graph


def script_11(project):
    # get degrees
    user_count = project.get_user_count()
    in_degrees, out_degrees = project.get_degrees()
    # convert to [in_degree, out_degree]
    pos = np.zeros((user_count, 2))
    for i, user in enumerate(in_degrees.keys()):
        pos[i, 0] = in_degrees[user]
        pos[i, 1] = out_degrees[user]
    # print(pos)
    # plot Kmeans
    plot_user_degree_KMeans_graph(pos)