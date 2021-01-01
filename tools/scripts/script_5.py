from tools.utils.plot_helpers import plot_net_graph


def script_5(project):
    # get actions
    actions = project.get_action_types()
    actions.append('all actions')
    # plot graph
    for action in actions:
        edge_count, edges = project.get_edges(action)
        if edge_count > 0:
            plot_net_graph(edges, title=f'net graph for {action}')