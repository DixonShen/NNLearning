# coding=utf8


__author__ = 'DixonShen'

list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b', 'c', 'd', 'e']
print [(a, b)
       for a in list1
       for b in list2[:-1]]
for i in range(len(list1)):
    print i
