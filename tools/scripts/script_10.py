import os
import csv


def script_10(project):
    # gen user_keyword_counts and user_keyword_frequencys
    user_keyword_counts, user_keyword_frequencys = \
        project.get_user_keyword_counts('./keywords.txt')
    # output as csv
    if not os.path.exists('./results'):
        os.mkdir('./results')
    with open('./results/user_keyword_counts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user', 'keyword_count', 'keyword_frequency'])
        for user in user_keyword_counts.keys():
            writer.writerow([user, user_keyword_counts[user], user_keyword_frequencys[user]])
    print(
        'Successfully output result to file: ./results/user_keyword_counts.csv'
    )