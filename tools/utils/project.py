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
        # fix space in user name
        for i in range(len(self.data['users'])):
            if isinstance(self.data['users'][i], str):
                self.data['users'][i] = self.data['users'][i].strip(' ')
            if isinstance(self.data['to_users'][i], str):
                self.data['to_users'][i] = self.data['to_users'][i].strip(' ')
        print('Successfully extract data')

    def get_user_count(self):
        """get user count

        Returns:
            user_count (int)
        """
        user_set = set(self.data['users'])
        return len(user_set)

    def get_users(self):
        """get users list

        Returns:
            users (list)
        """
        users = list(set(self.data['users']))
        return users

    def get_action_count(self):
        """get action count

        Returns:
            action_count (int)
        """
        action_set = set(self.data['actions'])
        return len(action_set)

    def get_action_types(self):
        """get action types list

        Returns:
            action_types (list)
        """
        self.action_types = list()
        for action in self.data['actions']:
            if action not in self.action_types:
                self.action_types.append(action)
        return self.action_types

    def get_action_counts_by_type(self):
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

    def get_action_user_counts_by_type(self):
        """get user counts of different actions

        Returns:
            action_user_counts (dict)
        """
        # gen user sets
        action_user_sets = dict()
        for user, action in zip(self.data['users'], self.data['actions']):
            if action not in action_user_sets:
                action_user_sets[action] = set()
            action_user_sets[action].add(user)
        # gen counts from sets
        action_user_counts = dict()
        for action, user_set in action_user_sets.items():
            action_user_counts[action] = len(user_set)
        return action_user_counts

    def get_action_counts_by_month(self):
        """get sum action counts by month

        Returns:
            action_counts (dict)
        """
        # deal with raw dates and gen action counts
        action_counts = dict()
        for date in self.data['dates']:
            new_date = '-'.join(date.split('-')[:2])
            if new_date not in action_counts:
                action_counts[new_date] = 0
            action_counts[new_date] += 1
        return action_counts

    def get_action_counts_by_year_and_type(self):
        """get counts of different actions by year

        Returns:
            action_counts: dict
        """
        # format like: {'date':{'type':count, ...}, ...}
        action_counts = dict()
        for date, action in zip(self.data['dates'], self.data['actions']):
            new_date = '-'.join(date.split('-')[:1])
            if new_date not in action_counts:
                action_counts[new_date] = dict()
            if action not in action_counts[new_date]:
                action_counts[new_date][action] = 0
            action_counts[new_date][action] += 1
        return action_counts

    def get_user_counts_by_month(self):
        """get user counts by month

        Returns:
            user_counts (dict)
        """
        # deal with raw dates and gen user sets
        user_sets = dict()
        for user, date in zip(self.data['users'], self.data['dates']):
            new_date = '-'.join(date.split('-')[:2])
            if new_date not in user_sets:
                user_sets[new_date] = set()
            user_sets[new_date].add(user)
        # get user counts from sets
        user_counts = dict()
        for date, user_set in user_sets.items():
            user_counts[date] = len(user_set)
        return user_counts

    def get_edges(self, action='all actions'):
        """get edges for graph drawing

        Args:
            action (str, optional): selected action to draw, avoid a too complex graph. Defaults to 'all actions'.

        Returns:
            edge_count (int)
            edges (dict)
        """
        # get users and actions
        users = self.get_users()
        actions = self.get_action_types()
        # get edge_count and edges dict
        # edges[user] is a dict list of all edges from user
        # dict(to=xx, weight=xx)
        edge_count = 0
        edges = dict()
        for user in users:
            edges[user] = list()
        for action_type in actions:
            edges[action_type] = list()
        # get edge and weight
        for from_user, edge_action, to_user in zip(self.data['users'],
                                                   self.data['actions'],
                                                   self.data['to_users']):
            # check action type
            if action != 'all actions' and edge_action != action:
                continue
            # check empty input
            if not isinstance(to_user, str):
                if edge_action in [
                        'created a topic', 'added a blogpost', 'added a design'
                ]:
                    to_user = edge_action
                else:
                    continue
            edge_count += 1
            # check whether exist
            flag = False
            for edge in edges[from_user]:
                if edge['to'] == to_user:
                    edge['weight'] += 1
                    flag = True
                    break
            # not exist then create new edge
            if flag is False:
                edges[from_user].append(dict(to=to_user, weight=1))
        return edge_count, edges

    def get_degrees(self):
        """get in_degrees and out_degrees for all users

        Returns:
            in_degrees (dict)
            out_degrees (dict)
        """
        # get users, edges and acitons
        actions = self.get_action_types()
        users = self.get_users()
        _, edges = self.get_edges()
        # cal degrees
        in_degrees = dict()
        out_degrees = dict()
        for user in users:
            in_degrees[user] = 0
            out_degrees[user] = 0
        for from_user, user_edges in edges.items():
            for edge in user_edges:
                out_degrees[from_user] += edge['weight']
                if edge['to'] not in actions:
                    in_degrees[edge['to']] += edge['weight']
        return in_degrees, out_degrees