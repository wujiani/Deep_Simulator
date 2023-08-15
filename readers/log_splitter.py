# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 21:35:36 2020

@author: Manuel Camargo
"""
import copy
import itertools
from operator import itemgetter
import numpy as np
import pandas as pd
import random


class LogSplitter(object):
    """
    This class reads and parse the elements of a given event-log
    expected format .xes or .csv
    """

    def __init__(self, log, verbose=True):
        """constructor"""
        self.log = pd.DataFrame(log)
        self._sort_log()

    def split_log(self, method: str, size: float, one_timestamp: bool):
        splitter = self._get_splitter(method)
        return splitter(size, one_timestamp)

    def _get_splitter(self, method):
        if method == 'timeline_contained':
            return self._timeline_contained
        elif method == 'timeline_trace':
            return self._timeline_trace
        elif method == 'random':
            return self._random
        else:
            raise ValueError(method)

    def _timeline_contained(self, size: float, one_timestamp: bool) -> None:

        grouped = self.log.groupby('caseid')['start_timestamp'].min().reset_index()
        # Sort the grouped dataframe by 'start_timestamp'
        sorted_grouped = grouped.sort_values(by='start_timestamp')
        # Calculate the number of cases to consider (80% of the total)
        total_cases = len(sorted_grouped)
        cases_to_select = int(0.8 * total_cases)
        # Select the first 80% of caseids and store them in a list
        caseid_train_list = sorted_grouped['caseid'][:cases_to_select].tolist()

        df_train = self.log[self.log['caseid'].isin(caseid_train_list)]
        df_test = self.log[~self.log['caseid'].isin(caseid_train_list)]

        df_test = (df_test
                   .sort_values(['caseid','pos_trace'], ascending=True)
                   .reset_index(drop=True))
        df_train = (df_train
                    .sort_values(['caseid','pos_trace'], ascending=True)
                    .reset_index(drop=True))

        df_test = df_test.drop(columns=['trace_len', 'pos_trace'])
        df_train = df_train.drop(columns=['trace_len', 'pos_trace'])
        return df_train, df_test

    def _timeline_trace(self, size: float, one_timestamp: bool) -> None:
        # log = self.log.data.to_dict('records')
        cases = self.log[self.log.pos_trace == 1]
        key = 'end_timestamp' if one_timestamp else 'start_timestamp'
        cases = cases.sort_values(key, ascending=False)
        cases = cases.caseid.to_list()
        num_test_cases = int(np.round(len(cases)*(1 - size)))
        test_cases = cases[:num_test_cases]
        train_cases = cases[num_test_cases:]
        df_train = self.log[self.log.caseid.isin(train_cases)]
        df_test = self.log[self.log.caseid.isin(test_cases)]
        df_train = df_train.drop(columns=['trace_len', 'pos_trace'])
        df_test = df_test.drop(columns=['trace_len', 'pos_trace'])
        return df_train, df_test

    def _random(self, size: float, one_timestamp: bool) -> None:
        cases = list(self.log.caseid.unique())
        sample_sz = int(np.ceil(len(cases)*size))
        scases = random.sample(cases, sample_sz)
        df_train = self.log[self.log.caseid.isin(scases)]
        df_test = self.log[~self.log.caseid.isin(scases)]
        return df_train, df_test

    def _sort_log(self):
        log = copy.deepcopy(self.log)
        log = sorted(log.to_dict('records'), key=lambda x: x['caseid'])
        for key, group in itertools.groupby(log, key=lambda x: x['caseid']):
            events = list(group)
            # events = sorted(events, key=itemgetter('end_timestamp'))
            length = len(events)
            for i in range(0, len(events)):
                events[i]['pos_trace'] = i + 1
                events[i]['trace_len'] = length
        log = pd.DataFrame.from_dict(log)
        log.sort_values(by='end_timestamp', ascending=False, inplace=True)
        self.log = log