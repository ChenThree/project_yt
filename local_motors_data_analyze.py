from tools.utils.project import Project
from tools.utils.get_script import get_script


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

    # use specific script to analyze
    script = get_script(analyze_type)
    script(project)


if __name__ == "__main__":
    main()
