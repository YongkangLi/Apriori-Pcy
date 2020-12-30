#!/usr/bin/python

from itertools import chain, combinations
from collections import defaultdict


def read_csv(csv):
    with open(csv, "r") as file_iter:
        for line in file_iter:
            line = line.split("{")
            line = line[len(line) - 1].split("}")
            line = line[len(line) - 2]
            line = line.strip().rstrip(",")
            record = frozenset(line.split(","))
            yield record


def parse(data_iterator):
    transactions = list()
    items = set()
    mapping = dict({})
    for record in data_iterator:
        transaction = frozenset(record)
        transactions.append(transaction)
        for item in transaction:
            items.add(frozenset([item]))
        i = 1
        for item in items:
            mapping[item] = i
            i += 1
    return items, transactions, mapping


def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def combine(items, length):
    return set([i.union(j) for i in items for j in items if len(i.union(j)) == length])


def threshold(items, transactions, min_support, freq):
    _itemSet = set()
    local = defaultdict(int)

    for item in items:
        for transaction in transactions:
            if item.issubset(transaction):
                freq[item] += 1
                local[item] += 1

    for item, count in local.items():
        support = float(count) / len(transactions)

        if support >= min_support:
            _itemSet.add(item)

    return _itemSet


def pcy(items, transactions, min_support, mapping, freq):
    _itemSet = set()
    local = defaultdict(int)

    n = 1024
    buckets = [0 for i in range(n)]

    for item in items:
        for transaction in transactions:
            if item.issubset(transaction):
                product = 1
                for thing in item:
                    product *= mapping[frozenset([thing])]
                buckets[product % n] += 1

    vector = 0
    for i in range(len(buckets)):
        if buckets[i] >= min_support * len(transactions):
            vector |= 1 << i
    print("{0:b}".format(vector))
    print(len(transactions))
    for item in items:
        product = 1
        for thing in item:
            product *= mapping[frozenset([thing])]
        # print(buckets[product % n])
        if buckets[product % n] < min_support * len(transactions):
            continue
        for transaction in transactions:
            if item.issubset(transaction):
                freq[item] += 1
                local[item] += 1

    for item, count in local.items():
        support = float(count) / len(transactions)

        if support >= min_support:
            _itemSet.add(item)

    return _itemSet


def apriori(data_iter, min_support, min_confidence):
    items, transactions, mapping = parse(data_iter)
    freq = defaultdict(int)
    large = dict()

    ones = threshold(items, transactions, min_support, freq)

    current = ones
    k = 2
    while current != set([]):
        large[k - 1] = current
        current = combine(current, k)
        if k == 2:
            current = pcy(current, transactions, min_support, mapping, freq)
        else:
            current = threshold(current, transactions, min_support, freq)
        current = current
        k = k + 1

    def get_support(item):
        return float(freq[item]) / len(transactions)

    items = []
    for key, value in large.items():
        items.extend([(tuple(item), get_support(item)) for item in value])

    rules = []
    for key, value in list(large.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = get_support(item) / get_support(element)
                    if confidence >= min_confidence:
                        rules.append(((tuple(element), tuple(remain)), confidence))
    return items, rules


def results(items, result, ones, twos, threes, fours, others, rules):
    f0 = open(rules, "w")
    f1 = open(ones, "w")
    f2 = open(twos, "w")
    f3 = open(threes, "w")
    f4 = open(fours, "w")
    fo = open(others, "w")

    for item, support in sorted(items, key=lambda x: x[1]):
        if len(item) == 1:
            f1.write("%s , %.3f\n" % (str(item), support))
        elif len(item) == 2:
            f2.write("%s , %.3f\n" % (str(item), support))
        elif len(item) == 3:
            f3.write("%s , %.3f\n" % (str(item), support))
        elif len(item) == 4:
            f4.write("%s , %.3f\n" % (str(item), support))
        else:
            fo.write("%s , %.3f\n" % (str(item), support))

    for rule, confidence in sorted(result, key=lambda x: x[1]):
        pre, post = rule
        f0.write("%s ==> %s , %.3f\n" % (str(pre), str(post), confidence))
