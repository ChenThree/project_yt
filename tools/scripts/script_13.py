from ..utils.plot_helpers import plot_bar_chart_by_keywords


def script_13(project):
    # get top5 keywords by year and draw bar chart
    sorted_keywords_by_year = project.get_top_keywords_by_year()
    print(sorted_keywords_by_year)
    plot_bar_chart_by_keywords(
        sorted_keywords_by_year,
        title='bar chart for keywords by year')