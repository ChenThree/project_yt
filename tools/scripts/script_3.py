from ..utils.plot_helpers import plot_pie_chart, plot_bar_chart, plot_bar_chart_by_types


def script_3(project):
    # get action counts and generate graph
    action_counts = project.get_action_counts_by_type()
    print('action_counts ==', action_counts)
    # pie chart
    plot_pie_chart(action_counts,
                   title='pie chart for action counts',
                   startangle=110,
                   swap=True)
    # bar chart by month
    action_counts = project.get_action_counts_by_month()
    plot_bar_chart(action_counts, title='bar chart for action counts by month')
    # bar chart by year and type
    action_types = project.get_action_types()
    action_counts = project.get_action_counts_by_year_and_type()
    plot_bar_chart_by_types(
        action_counts,
        action_types,
        title='bar chart for action counts by type and year')
