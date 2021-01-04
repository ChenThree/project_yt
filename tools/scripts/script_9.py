from tools.utils.plot_helpers import plot_wordcloud


def script_9(project):
    # get total count and words
    total_count, words = project.get_words()
    # print(word_counts)
    print('total word counts =', total_count)
    # plot wordcloud
    plot_wordcloud(words)