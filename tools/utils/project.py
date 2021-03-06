import pandas
import numpy as np
import jieba
import re


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

    def get_user_keyword_counts(self, keyword_path):
        """get user key word counts and frequencys

        Args:
            keywords (str): input keyword list path

        Returns:
            user_keyword_counts (dict) 
            user_keyword_frequencys (dict)
        """
        # read in keywords
        keywords = list()
        with open(keyword_path, 'r') as f:
            content = f.readlines()
        for line in content:
            keywords.append(line.strip('\n'))
        # get users and user_contents
        users = self.get_users()
        user_contents = dict()
        for user in users:
            user_contents[user] = ''
        for user, content in zip(self.data['users'], self.data['contents']):
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
                user_keyword_frequencys[user] += user_contents[user].count(
                    keyword)
                if keyword in user_contents[user]:
                    user_keyword_counts[user] += 1
        return user_keyword_counts, user_keyword_frequencys

    def get_user_impacts(self, keyword_path):
        """get user impact by degrees and keyword_counts

        Args:
            keywords (str): input keyword list path

        Returns:
            user_impacts (dict)
        """
        # get degrees and user keyword_counts
        in_degrees, out_degrees = self.get_degrees()
        user_keyword_counts, _ = self.get_user_keyword_counts(keyword_path)
        # get impacts
        user_impacts = dict()
        for user in in_degrees.keys():
            user_impacts[user] = in_degrees[user] * 0.6 + \
                out_degrees[user] * 0.3 + user_keyword_counts[user] * 0.1
        return user_impacts

    def get_stopwords(self, stopword_path):
        """get stopwords from file

        Args:
            stopword_path (str): path for stopwords file

        Returns:
            stopwords (list)
        """
        # read in stopwords
        stopwords = list()
        with open(stopword_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
        for line in content:
            stopwords.append(line.strip('\n'))
        return stopwords

    def get_words(self):
        """get words by jieba and re

        Returns:
            total_count (int)
            words (list)
        """
        # use jieba to cut word
        word_counts = dict()
        words = list()
        total_count = 0
        # del stop words
        stopwords = self.get_stopwords('./stopwords.txt')
        # use re to filter words
        r = re.compile('[a-zA-Z]+\'*[a-z]*')
        for content in self.data['contents']:
            # avoid empty input
            if not isinstance(content, str):
                continue
            for word in jieba.cut(content):
                if re.match(r, word) is None or word in stopwords:
                    continue
                if word not in word_counts:
                    word_counts[word] = 0
                word_counts[word] += 1
                words.append(word)
                total_count += 1
        return total_count, words

    def get_top_keywords_by_year(self):
        """get sorted top5 keywords by year

        Returns:
            sorted_keywords_by_year (dict)
        """
        # get contents by year
        contents_by_year = dict()
        for date, content in zip(self.data['dates'], self.data['contents']):
            # check empty content
            if not isinstance(content, str):
                continue
            # get year
            year = date.split('-')[0]
            if year not in contents_by_year:
                contents_by_year[year] = ''
            else:
                contents_by_year[year] += ' ' + content
        # del abbr word
        stopwords = self.get_stopwords('./stopwords.txt')
        # use re to filter words
        r = re.compile('[a-zA-Z]+\'*[a-z]*')
        # get top keywords
        word_counts = dict()
        for year, content in contents_by_year.items():
            word_counts[year] = dict()
            for word in jieba.cut(content):
                if re.match(r, word) is None or word in stopwords:
                    continue
                if word not in word_counts[year]:
                    word_counts[year][word] = 0
                word_counts[year][word] += 1
        # get sorted result
        sorted_keywords_by_year = dict()
        for year, word_counts_by_year in word_counts.items():
            sorted_keywords_by_year[year] = dict()
            sorted_word_counts = sorted(word_counts_by_year.items(), key=lambda d:d[1], reverse=True)
            for i in range(5):
                sorted_keywords_by_year[year][sorted_word_counts[i][0]] = sorted_word_counts[i][1]
        return sorted_keywords_by_year
