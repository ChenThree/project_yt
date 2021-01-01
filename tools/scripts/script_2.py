from ..utils.plot_helpers import plot_line_chart


def script_2(project):
    # get user counts by month
    user_counts = project.get_user_counts_by_month()
    print(user_counts)
    # plot
    plot_line_chart(user_counts, title='line chart for user by month')