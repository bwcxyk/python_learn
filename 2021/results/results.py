#!/bin/env python


# A 90-100
# B 80-89
# C 60-79
# D 40-59
# E 0-39

results = int(input("results:"))

if results > 90:
    print("A")
elif 89 > results > 80:
    print("B")
elif 79 > results > 60:
    print("C")
elif 59 > results > 40:
    print("D")
else:
    print("E")
