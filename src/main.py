#!/usr/bin/python

import sys
from optparse import OptionParser
import apriori

opt_parser = OptionParser()
opt_parser.add_option("-f", "--inputFile", dest="input", help="filename containing csv", default=None)
opt_parser.add_option("-s", "--minSupport", dest="minS", help="minimum support value", default=0.005, type="float")
opt_parser.add_option("-c", "--minConfidence", dest="minC", help="minimum confidence value", default=0.5, type="float")
opt_parser.add_option("-1", "--ones", dest="ones", help="dest file for one", default="../data/ones", type="str")
opt_parser.add_option("-2", "--twos", dest="twos", help="dest file for one", default="../data/twos", type="str")
opt_parser.add_option("-3", "--threes", dest="threes", help="dest file for one", default="../data/threes", type="str")
opt_parser.add_option("-4", "--fours", dest="fours", help="dest file for one", default="../data/fours", type="str")
opt_parser.add_option("-o", "--others", dest="others", help="dest file for one", default="../data/others", type="str")
opt_parser.add_option("-r", "--rules", dest="rules", help="dest file for rules", default="../data/rules", type="str")

(options, args) = opt_parser.parse_args()

inFile = None
if options.input is None:
    inFile = sys.stdin
elif options.input is not None:
    inFile = apriori.read_csv(options.input)
else:
    print("No dataset filename specified, system with exit\n")
    sys.exit("System will exit")

min_support = options.minS
min_confidence = options.minC
ones = options.ones
twos = options.twos
threes = options.threes
fours = options.fours
others = options.others
rules = options.rules

items, result = apriori.apriori(inFile, min_support, min_confidence)

apriori.results(items, result, ones, twos, threes, fours, others, rules)
