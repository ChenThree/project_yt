import pandas
import numpy as np


class Project:
    """class for the whole project
    """
    def __init__(self, data_path):
        """read in an excel file and extract data to create new project

        Args:
            data_path (str): excel file path

        Raises:
            RuntimeError: Error reading excel file
        """
        # read in data
        try:
            raw_datas = pandas.read_excel(data_path, engine='openpyxl').values
        except Exception as e:
            raise RuntimeError(f'Error reading excel file {data_path}:\n{e}')
        # remove empty line
        valid_line_count = 0
        while isinstance(raw_datas[valid_line_count, 0], str):
            valid_line_count += 1
        raw_datas = np.delete(raw_datas, slice(valid_line_count, None), axis=0)
        # remove empty column
        valid_column_count = 7
        raw_datas = np.delete(raw_datas,
                              slice(valid_column_count, None),
                              axis=1)
        # get valid input size
        w, h = np.shape(raw_datas)
        print(f'Read in excel data size: {w}*{h}')
        # extract data
        self.data = dict(users=list(raw_datas[:, 0]),
                         dates=list(raw_datas[:, 1]),
                         actions=list(raw_datas[:, 2]),
                         urls=list(raw_datas[:, 3]),
                         contents=list(raw_datas[:, 4]),
                         to_users=list(raw_datas[:, 5]),
                         topic_ids=list(raw_datas[:, 6]))
        # fix actions with 2 spaces
        for i in range(len(self.data['actions'])):
            self.data['actions'][i] = self.data['actions'][i].replace(
                '  ', ' ')
        print('Successfully extract data')

    def get_user_count(self):
        """get user count

        Returns:
            user_count (int)
        """
        user_set = set(self.data['users'])
        return len(user_set)

    def get_action_counts(self):
        """get counts of different actions

        Returns:
            action_counts (dict)
        """
        action_counts = dict()
        for action in self.data['actions']:
            if action not in action_counts:
                action_counts[action] = 0
            action_counts[action] += 1
        return action_counts
