import jieba

from tools.utils.plot_helpers import plot_wordcloud


def script_9(project):
    # use jieba to cut word
    word_counts = dict()
    words = list()
    total_count = 0
    for content in project.data['contents']:
        # avoid empty input
        if not isinstance(content, str):
            continue
        for word in jieba.cut(content):
            if word not in word_counts:
                word_counts[word] = 0
            word_counts[word] += 1
            words.append(word)
            total_count += 1
    print('total word counts =', total_count)
    # plot wordcloud
    plot_wordcloud(words)