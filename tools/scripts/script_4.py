from ..utils.plot_helpers import plot_line_chart

def script_4(project):
    # print action count
    print('action_count ==', project.get_action_count())
    # bar chart by month
    action_counts = project.get_action_counts_by_month()
    plot_line_chart(action_counts, title='line chart for action counts by month')