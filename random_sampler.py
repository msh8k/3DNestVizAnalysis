from pymongo import MongoClient
import csv
import pprint

client = MongoClient()

ten = [str(x) for x in range(10, 501, 10)]
hundred = [str(y) for y in range(100, 5001, 100)]

db_read = client['max_wall_const']
db_write = client['analysis']

coll_write = db_write['max_wall_10']
for c in ten:
    coll = db_read[c]
    coll_write.insert(coll.aggregate([{'$sample': {'size': 10}}]))


coll_write = db_write['max_wall_100']
for c in hundred:
    coll = db_read[c]
    coll_write.insert(coll.aggregate([{'$sample': {'size': 10}}]))


# with open('max_age_cell_counts.csv', 'w', newline='') as csvfile:
#     randwriter = csv.writer(csvfile)
#     randwriter.writerow(num_cells)
