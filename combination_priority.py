import itertools


class CombinationPriority:
    def __new__(self):

        # Get all possible combinations
        all_combinations = list(itertools.product('0ope', repeat=5))
        comb_list = []

        # Make strings from tuples and append them to new list
        for comb in all_combinations:
            comb_list.append(''.join(comb))

        comb_list = list(filter(lambda c: c[0] not in ('0', 'e') and
                                not c.count('0') == 0 and
                                not (c.count('e') == 4 and c[1:] == 'eeee') and
                                not (c.count('e') == 3 and c[2:] == 'eee') and
                                not (c.count('e') == 2 and c[3:] == 'ee') and
                                not (c.count('e') == 1 and c[4] == 'e'),
                                comb_list))

        comb_priority_dict = {}
        for i in range(10):
            comb_priority_dict[str(i)] = []

        unused_comb = []
        for c in comb_list:
            if c.count('p') == 4 and c.count('0') == 1:
                comb_priority_dict['0'].append(c)
            elif c.count('o') == 4 and c.count('0') == 1:
                comb_priority_dict['1'].append(c)
            elif c.count('p') == 3 and c.count('0') == 2:
                comb_priority_dict['2'].append(c)
            elif c.count('o') == 3 and c.count('0') == 2:
                comb_priority_dict['4'].append(c)
            elif c.count('p') == 2:
                comb_priority_dict['5'].append(c)
            elif c.count('o') == 2:
                comb_priority_dict['6'].append(c)
            elif c.count('p') == 1 or c.count('o') == 1:
                comb_priority_dict['7'].append(c)
            elif c.count('e') == 1:
                comb_priority_dict['8'].append(c)
            elif c.count('e') >= 2:
                comb_priority_dict['9'].append(c)
            else:
                unused_comb.append(c)

        # Check if all combinations have been used
        if __name__ == "__main__":
            print('Unused combinations:', len(unused_comb), '\n', unused_comb)

        return comb_priority_dict


print(CombinationPriority())