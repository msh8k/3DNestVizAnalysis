from pymongo import MongoClient
import csv

client = MongoClient()

ten = [str(x) for x in range(10, 501, 10)]
hundred = [str(y) for y in range(100, 5001, 100)]

db_read = client['analysis']

outer_walls = []
cell_count = []
compactness = []

coll = db_read['hybrid_height_100']
cursor = coll.find()

for doc in cursor:
    cell_count.append(len(doc['Cells']))
    outer_walls.append(doc['Outer Walls'])
    compactness.append(doc['2D Compactness'])


with open('hybrid_height_100.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(cell_count)
    csvwriter.writerow(outer_walls)
    csvwriter.writerow(compactness)
