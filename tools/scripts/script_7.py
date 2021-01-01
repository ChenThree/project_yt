import os
import csv


def script_7(project):
    # get action counts
    action_user_counts = project.get_action_user_counts_by_type()
    print('action_user_counts ==', action_user_counts)
    # output as csv
    if not os.path.exists('./results'):
        os.mkdir('./results')
    with open('./results/action_user_counts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['action type', 'user_count'])
        for action, user_count in action_user_counts.items():
            writer.writerow([action, user_count])
    print(
        'Successfully output result to file: ./results/action_user_counts.csv')
