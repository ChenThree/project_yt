import os
import csv


def script_12(project):
    # get user_impacts
    user_impacts = project.get_user_impacts('./keywords.txt')
    # print(user_impacts)
    # output as csv
    if not os.path.exists('./results'):
        os.mkdir('./results')
    with open('./results/user_impacts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user', 'impact'])
        for user in user_impacts.keys():
            writer.writerow([user, user_impacts[user]])
    print(
        'Successfully output result to file: ./results/user_impacts.csv'
    )