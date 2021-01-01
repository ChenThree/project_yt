import os
import csv


def script_10(project):
    # read in keywords
    keywords = list()
    with open('./keywords.txt', 'r') as f:
        content = f.readlines()
    for line in content:
        keywords.append(line.strip('\n'))
    # get users and user_contents
    users = project.get_users()
    user_contents = dict()
    for user in users:
        user_contents[user] = ''
    for user, content in zip(project.data['users'], project.data['contents']):
        # check empty content
        if not isinstance(content, str):
            continue
        user_contents[user] += ' ' + content
    # gen user_keyword_counts and user_keyword_frequencys
    user_keyword_counts = dict()
    user_keyword_frequencys = dict()
    for user in users:
        user_keyword_counts[user] = 0
        user_keyword_frequencys[user] = 0
    for keyword in keywords:
        for user in users:
            user_keyword_frequencys[user] += user_contents[user].count(keyword)
            if keyword in user_contents[user]:
                user_keyword_counts[user] += 1
    # output as csv
    if not os.path.exists('./results'):
        os.mkdir('./results')
    with open('./results/user_keyword_counts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user', 'keyword_count', 'keyword_frequency'])
        for user, keyword_count, keyword_frequency in zip(
                user_keyword_counts.keys(), user_keyword_counts.values(),
                user_keyword_frequencys.values()):
            writer.writerow([user, keyword_count, keyword_frequency])
    print(
        'Successfully output result to file: ./results/user_keyword_counts.csv'
    )
