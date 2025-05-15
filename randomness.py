from pymongo import MongoClient
from matplotlib import pyplot as plt
from pprint import pprint
import numpy as np
import csv

client = MongoClient()

db = client['randomness_validation']

coll = db['tests']

cursor = coll.find()

tests = []
test = []

for doc in cursor:
    tests.append(doc['Percentages'])

mean = np.mean(tests, axis=0)
var = np.var(tests, axis=0)
std = np.std(tests, axis=0)

with open('randomness_stats.csv', 'w', newline='') as csvfile:
    randwriter = csv.writer(csvfile)
    randwriter.writerow(mean)
    randwriter.writerow(std)

# print(len(mean))
# print(mean)
#
# print(len(var))
# print(var)
#
# print(len(std))
# print(std)