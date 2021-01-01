from utils.project import Project
from utils.plot_helpers import plot_pie_chart

def main():
    # read in data
    data_path = './data/1112 RF(2).xlsx'
    project = Project(data_path)

    # start analyze by input int
    analyze_type = input('Input a int choose analyze type ( 1 ~ 13 ): ')
    try:
        analyze_type = int(analyze_type)
        if analyze_type not in range(1, 14):
            raise Exception
    except Exception:
        raise ValueError('Please input int in 1 ~ 13')

    # print user count
    print('user_count ==', project.get_user_count())
    # get action counts and generate graph
    action_counts = project.get_action_counts()
    print('action_counts ==', action_counts)
    plot_pie_chart(action_counts,
                   title='pie chart for action counts',
                   startangle=110,
                   swap=True)


if __name__ == "__main__":
    main()
