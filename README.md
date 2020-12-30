# Apriori-Pcy
Relationship Mining via Apriori and Pcy in python


Usage:

```
$ ./main.py -f ./data/Groceries.csv -s [min-support] -c [min-confidence] -1 [one-set] -2 [two-set] -3 [three-set] -4 [four-set] -o [other-set] -r [rules]
```

Example:

```
    $ ./main.py -f ../data/Groceries.csv -s 0.005 -c 0.5 -1 ../data/ones -2 ../data/twos -3 ../data/threes -4 ../data/fours -o ../data/others, -r ../data/rules 
```
