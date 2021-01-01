from ..utils.plot_helpers import plot_pie_chart

def script_2(project):
    # get action counts and generate graph
    action_counts = project.get_action_counts()
    print('action_counts ==', action_counts)
    plot_pie_chart(action_counts,
                   title='pie chart for action counts',
                   startangle=110,
                   swap=True)