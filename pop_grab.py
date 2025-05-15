from pymongo import MongoClient
# from collections import defaultdict
# from matplotlib import pyplot as PLT
from matplotlib import cm
# from matplotlib import mlab as ML
# import numpy as NP
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

import csv

client = MongoClient()

ten = [str(x) for x in range(10, 501, 10)]
hundred = [str(y) for y in range(100, 5001, 100)]

db_read = client['random_const']

# outer_walls = defaultdict(list)
# compactness = defaultdict(list)

outer_walls = []
num_cells = []

for c in ten:
    coll = db_read[c]
    cursor = coll.find()

    for doc in cursor:
        num_cells.append(len(doc['Cells']))
        outer_walls.append(doc['Outer Walls'])
        # outer_walls[(len(doc['Cells']))].append(doc['Outer Walls'])
        # compactness.append((len(doc['Cells']), doc['2D Compactness']))

n_cells = []
o_walls = []

db = client['analysis']
coll = db['random_10']
cursor = coll.find()

for doc in cursor:
    n_cells.append(len(doc['Cells']))
    o_walls.append(doc['Outer Walls'])

x = np.asarray(num_cells)
y = np.asarray(outer_walls)

# Calculate the point density
xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = x[idx], y[idx], z[idx]

s_x = np.asarray(n_cells)
s_y = np.asarray(o_walls)

s_xy = np.vstack([s_x, s_y])
s_z = gaussian_kde(s_xy)(s_xy)

s_idx = s_z.argsort()
s_x, s_y, s_z = s_x[s_idx], s_y[s_idx], s_z[s_idx]

fig, ax = plt.subplots()
heatmap = ax.scatter(x, y, c=z, cmap=cm.jet, s=20, edgecolor='face', alpha=1, zorder=1)

cb1 = fig.colorbar(heatmap, ticks=[0.0000127, 0.000382], orientation='horizontal')
cb1.ax.set_xticklabels(['Low', 'High'])
cb1.ax.set_xlabel('Population Concentration')

sample = ax.scatter(s_x, s_y, c=s_z, cmap=cm.binary, s=4, zorder=2)
# sample = ax.scatter(n_cells, o_walls, c='0.5', s=4, marker='o', zorder=2)

cb2 = fig.colorbar(sample, ticks=[0.00002, 0.00037], orientation='horizontal')
cb2.ax.set_xticklabels(['Low', 'High'])
cb2.ax.set_xlabel('Sample Concentration')

plt.xlabel('Number of Cells')
plt.ylabel('Compactness')
plt.title('Random Rule Heat Map: 10 - 500 Pulp Loads')

plt.show()

# outer_walls.sort(key=lambda nest: nest[0])
#
# work = []
# outer_one_dev = {}
# outer_two_dev = {}

# for i in range(190):
#     if i == outer_walls[0][0]:
#         work.append(outer_walls.pop(0))

# with open('random_pop_10.csv', 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(outer_walls.keys)
#     csvwriter.writerow(outer_walls.values)
#     csvwriter.writerow(compactness.values)



# n = 1e5
# x = y = NP.linspace(-5, 5, 100)
# X, Y = NP.meshgrid(x, y)
# Z1 = ML.bivariate_normal(X, Y, 2, 2, 0, 0)
# Z2 = ML.bivariate_normal(X, Y, 4, 1, 1, 1)
# ZD = Z2 - Z1
# x = X.ravel()
# y = Y.ravel()
# z = ZD.ravel()
# gridsize=30
# PLT.subplot(111)

# if 'bins=None', then color of each hexagon corresponds directly to its count
# 'C' is optional--it maps values to x-y coordinates; if 'C' is None (default) then
# the result is a pure 2D histogram

# PLT.hexbin(x, y, C=z, gridsize=gridsize, cmap=CM.jet, bins=None)
# plt.hexbin(num_cells, outer_walls, gridsize=35, cmap=cm.jet, bins=11)
# cb = plt.colorbar()
# cb.set_label('Points per Bin')
#
# PLT.scatter(n_cells, o_walls, s=4)
# PLT.axis([0, 300, 0, 300])
