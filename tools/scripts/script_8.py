from ..utils.plot_helpers import plot_pie_chart


def script_8(project):
    # get action counts and generate graph
    action_user_counts = project.get_action_user_counts_by_type()
    print('action_user_counts ==', action_user_counts)
    # pie chart
    plot_pie_chart(action_user_counts,
                   title='pie chart for action user counts',
                   startangle=0,
                   swap=True)