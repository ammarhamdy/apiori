

class RuleGenerator:
    def __init__(self, meta_data_dict, number_of_transactions, most_freq_set, min_sup, min_conf):
        self.meta_data_dict = meta_data_dict
        self.number_of_transactions = number_of_transactions
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.most_freq_set = most_freq_set
        self.rules = list()
        self.generate(self.most_freq_set)

    def generate(self, values_set):
        if len(values_set) < 2:
            return
        for value in values_set:
            values = values_set.difference((value,))
            count_x_y = self.count_x_y_of(values, value)
            count_x = self.count_x_y_of(values)
            support = self.support_of(count_x_y)
            confidence = self.confidence_of(count_x_y, count_x)
            if support >= self.min_sup and confidence >= self.min_conf:
                self.rules.append((values, value, support, confidence))
            self.generate(values)

    def count_x_y_of(self, x, y=None):
        value_list = list(x)
        value_list.append(y)
        s = self.meta_data_dict[value_list[0]][1]
        for l in range(len(value_list) - (1 + (not y))):
            s = s.intersection(self.meta_data_dict[value_list[l + 1]][1])
        return len(s)

    def support_of(self, count_x_y):
        return count_x_y / self.number_of_transactions

    def confidence_of(self, count_x_y, count_x):
        return count_x_y / count_x



# if __name__ == '__main__':
#     rg = RuleGenerator(frozenset({'milke', 'eeg', 'bread'}), None, None, None)
#     for i in rg.rules:
#         print(i)
#     print(len(rg.rules))
