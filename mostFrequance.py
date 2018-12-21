from collections import OrderedDict
import time


def save(items: dict, file):
    file.write('sub item:\n')
    for item in items.items():
        file.write('   '+str(tuple(item[0])).ljust(30)+'\t'+str(item[1])+'\n')
    file.write('\n')


class MostFreq:
    def __init__(self, meta_data_dict, min_sup, save_ok=False):
        self.meta_data_dict = meta_data_dict
        self.min_sup = min_sup
        self.save_ok = save_ok
        self.most_freq_dict = self.most_freq_item()
        self.most_freq_set = list(self.most_freq_dict.keys())[0]
        self.count_of_most_freq = list(self.most_freq_dict.values())[0]

    def scan(self, items: OrderedDict, length):
        new_items = OrderedDict()
        items_value = list(items.items())
        threshold = len(items_value[0][0]) + 1
        for i in range(length - 1):
            for j in range(length - i - 1):
                value = items_value[i][0].union(items_value[j + i + 1][0])
                if len(value) > threshold:
                    continue
                count = self.count_of(list(value))
                if count < self.min_sup:
                    continue
                new_items[value] = count
        return new_items

    def main_items(self):
        items = OrderedDict()
        for key in self.meta_data_dict.keys():
            if self.meta_data_dict[key][0] >= self.min_sup:
                items[frozenset((key,))] = self.meta_data_dict[key][0]
        return items

    def most_freq_item(self):
        items = self.main_items()
        if self.save_ok:
            file = open(str(time.time()) + 'items.txt', mode='w')
            save(items, file)
            while len(items) > 1:
                sub_item = self.scan(items, len(items.keys()))
                save(sub_item, file)
                items = sub_item
            file.close()
        else:
            while len(items) > 1:
                sub_item2 = self.scan(items, len(items.keys()), )
                items = sub_item2
        return items

    def count_of(self, value_list):
        s = self.meta_data_dict[value_list[0]][1]
        for l in range(len(value_list) - 1):
            s = s.intersection(self.meta_data_dict[value_list[l + 1]][1])
        return len(s)
