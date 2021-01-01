import numpy as np
import wordcloud
import networkx as nx
from matplotlib import pyplot
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


def plot_pie_chart(counts, title='pie chart', startangle=0, swap=False):
    """plot pie chart according to input counts dict

    Args:
        counts (dict): input dict for counts
        startangle (int): start angle for the pie
        swap (boolean): whether swap the first one and last one

    Raises:
        ValueError: Input counts should be a dict
    """
    # check input
    if not isinstance(counts, dict):
        raise ValueError('Input counts should be a dict')
    # get keys list and values list from input dict
    keys = list()
    values = list()
    for key, value in counts.items():
        keys.append(key)
        values.append(value)
    # change order to get best show
    if swap is True:
        keys[0], keys[-1] = keys[-1], keys[0]
        values[0], values[-1] = values[-1], values[0]
        keys[2], keys[-3] = keys[-3], keys[2]
        values[2], values[-3] = values[-3], values[2]
    # plot
    pyplot.figure(figsize=(20, 10))
    pyplot.title(title)
    pyplot.pie(values,
               labels=keys,
               autopct='%1.1f%%',
               labeldistance=1.1,
               startangle=startangle)
    pyplot.legend(keys, loc='upper right')
    pyplot.axis('equal')
    pyplot.get_current_fig_manager().window.state('zoomed')
    pyplot.show()


def plot_line_chart(counts, title='line chart'):
    """plot line chart according to input counts dict

    Args:
        counts (dict): input counts dict by month
        title (str, optional): title for the figure. Defaults to 'line chart'.

    Raises:
        ValueError: Input counts should be a dict
    """
    # check input
    if not isinstance(counts, dict):
        raise ValueError('Input counts should be a dict')
    # get keys list and values list from input dict
    keys = list()
    values = list()
    for key, value in counts.items():
        keys.append(key)
        values.append(value)
    # plot
    pyplot.figure(figsize=(20, 10))
    pyplot.title(title)
    pyplot.plot(keys, values)
    pyplot.xticks(rotation=70)  # not overlap
    pyplot.get_current_fig_manager().window.state('zoomed')
    pyplot.show()


def plot_bar_chart(counts, title='bar chart'):
    """plot bar chart

    Args:
        counts (dict): intput counts dict
        title (str, optional): title for figure. Defaults to 'bar chart'.

    Raises:
        ValueError: Input counts should be a dict
    """
    # check input
    if not isinstance(counts, dict):
        raise ValueError('Input counts should be a dict')
    # get keys list and values list from input dict
    keys = list()
    values = list()
    for key, value in counts.items():
        keys.append(key)
        values.append(value)
    # plot
    pyplot.figure(figsize=(20, 10))
    pyplot.title(title)
    pyplot.bar(keys, values)
    pyplot.xticks(rotation=70)  # not overlap
    pyplot.get_current_fig_manager().window.state('zoomed')
    pyplot.show()


def plot_bar_chart_by_types(counts, action_types, title='bar chart'):
    """plot bar chart by type and time (multi bars)

    Args:
        counts (dict): input counts dict
        action_types (list): given types
        title (str, optional): title for figure. Defaults to 'bar chart'.

    Raises:
        ValueError: Input counts should be a dict
    """
    # check input
    if not isinstance(counts, dict):
        raise ValueError('Input counts should be a dict')
    # get keys list and values list from input dict
    keys = list()
    values = dict()
    for action_type in action_types:
        values[action_type] = list()
    for key, value in counts.items():
        keys.append(key)
        for action_type in action_types:
            values[action_type].append(value.get(action_type, 0))
    # plot
    pyplot.figure(figsize=(20, 10))
    pyplot.title(title)
    offset = 0
    for _, value in values.items():
        pyplot.bar(np.arange(len(keys)) + offset, value, width=0.07)
        offset += 0.07
    pyplot.xticks(ticks=np.arange(len(keys)) + 0.3, labels=keys)
    pyplot.legend(action_types, loc='upper right')
    pyplot.get_current_fig_manager().window.state('zoomed')
    pyplot.show()


def plot_wordcloud(words):
    """plot wordcloud according to input words list

    Args:
        words (list): words list
    """
    # gen wordcloud
    cloud = wordcloud.WordCloud(max_words=35)
    cloud.generate(' '.join(words))
    # plot
    pyplot.figure(figsize=(10, 5))
    pyplot.imshow(cloud)
    pyplot.xticks([])  # no show
    pyplot.yticks([])  # no show
    pyplot.title('wordcloud for contents')
    pyplot.get_current_fig_manager().window.state('zoomed')
    pyplot.show()


def plot_net_graph(edges, title='net graph'):
    """plot net graph according to input edges

    Args:
        edges (dict): input edges
        title (str, optional): figure title. Defaults to 'net graph'.
    """
    # create graph
    G = nx.Graph()
    # insert edge
    for from_user, user_edges in edges.items():
        for edge in user_edges:
            G.add_edge(from_user, edge['to'], weight=edge['weight'])
    # plot graph
    pyplot.figure(figsize=(20, 20))
    pos = nx.spring_layout(G, k=0.5, iterations=100)
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='red')
    nx.draw_networkx_edges(G, pos, width=2, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=10)
    weights = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, font_size=7)
    pyplot.get_current_fig_manager().window.state('zoomed')
    pyplot.title(title)
    pyplot.axis('equal')
    pyplot.show()


def plot_user_degree_KMeans_graph(pos, title='user degree Kmeans graph'):
    """KMeans to get user cluster

    Args:
        pos (np.array): input [x, y]
        title (str, optional): figure title. Defaults to 'user degree Kmeans graph'.
    """
    # rescale
    mms = MinMaxScaler()
    pos = mms.fit_transform(pos)
    # KMeans
    clf = KMeans(n_clusters=3)
    clf.fit(pos)
    labels = clf.labels_
    # plot
    color = ['r', 'g', 'b']
    for i in range(len(labels)):
        pyplot.scatter(pos[i, 0], pos[i, 1], c=color[labels[i]])
    pyplot.title(title)
    pyplot.xlim((-0.2, 1.2))
    pyplot.ylim((-0.2, 1.2))
    pyplot.xlabel('scaled in degree')
    pyplot.ylabel('scaled out degree')
    pyplot.show()
