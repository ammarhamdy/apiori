from mostFrequance import MostFreq
from ruleGenerator import RuleGenerator
from collections import OrderedDict
import csv


def meta_data_dict_of(data, length):
    od = OrderedDict()
    for index in range(length):
        for item in data[index]:
            od.setdefault(item, [0, set()])
            od[item][1].add(index)
            od[item][0] = od[item][0] + 1
    return od


class Apiori:
    def __init__(self, data_csv_path, mini_support, mini_confidence):
        self.data = list(csv.reader(open(data_csv_path)))
        #
        self.number_of_transactions = len(self.data)
        self.mini_support = int(mini_support*self.number_of_transactions)
        self.mini_confidence = mini_confidence
        #
        self.meta_data_dict = meta_data_dict_of(self.data, self.number_of_transactions)
        self.most_feq_set = MostFreq(self.meta_data_dict, self.mini_support, True).most_freq_set
        self.rules = RuleGenerator(self.meta_data_dict, self.number_of_transactions, self.most_feq_set,
                                   mini_support, self.mini_confidence).rules


if __name__ == '__main__':
    mini_sup = float(input('minimum support:'))
    mini_conf = float(input('minimum confidence:'))
    apiori = Apiori('data\\10.csv', mini_sup, mini_conf)
    print(tuple(apiori.most_feq_set))
    for it in apiori.rules:
        print(tuple(it[0]), '-->', it[1], '(', it[2], ',', it[3], ')')
