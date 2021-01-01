from ..utils.plot_helpers import plot_pie_chart

def script_2(project):
    # gget user counts by month
    user_counts = project.get_user_counts_by_month()
    print(user_counts)