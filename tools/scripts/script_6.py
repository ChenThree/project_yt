import os
import csv


def script_6(project):
    # get degrees
    in_degrees, out_degrees = project.get_degrees()
    # print(in_degrees)
    # print(out_degrees)
    # output as csv
    if not os.path.exists('./results'):
        os.mkdir('./results')
    with open('./results/degrees.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user', 'in_degree', 'out_degree'])
        for user, in_degree, out_degree in zip(in_degrees.keys(),
                                               in_degrees.values(),
                                               out_degrees.values()):
            writer.writerow([user, in_degree, out_degree])
    print('Successfully output result to file: ./results/degrees.csv')
