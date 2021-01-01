import numpy as np
import wordcloud

from matplotlib import pyplot


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
    pyplot.xticks(ticks=np.arange(len(keys)) + 0.2, labels=keys)
    pyplot.legend(action_types, loc='upper right')
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
    pyplot.xticks([]) # no show
    pyplot.yticks([]) # no show
    pyplot.title('wordcloud for contents')
    pyplot.show()