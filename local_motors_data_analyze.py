from matplotlib import pyplot
 
from project import Project

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
    pyplot.figure(figsize=(20,10))
    pyplot.title(title)
    pyplot.pie(values, 
        labels=keys, 
        autopct='%1.1f%%', 
        labeldistance=1.1,
        startangle=startangle)
    pyplot.legend(keys, loc='upper right')
    pyplot.axis('equal')
    pyplot.show()


if __name__ == "__main__":
    # read in data
    data_path = './1112 RF(2).xlsx'
    project = Project(data_path)
    # print user count
    print('user_count ==', project.get_user_count())
    # get action counts and generate graph
    action_counts = project.get_action_counts()
    print('action_counts ==', action_counts)
    plot_pie_chart(action_counts, 
        title='pie chart for action counts',
        startangle=110,
        swap=True)