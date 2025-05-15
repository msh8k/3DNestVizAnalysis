from vpython import *
from pymongo import *
from time import sleep

import random

WIDTH = 1200
HEIGHT = 900


class Mongo:
    def __init__(self):
        self.client = MongoClient()
        self.database_names = self.client.database_names()

    def get_database_pick(self, choice):
        self.database = self.client[choice]

    def get_collection_pick(self, choice):
        self.collection = self.database[choice]


scene.width = 0
scene.height = 0
scene.range = 0
scene.title = "Nest Visualizer (IN 3D!)\n"


def send_b1(m):
    mongo.get_database_pick(m.selected)
    print(m.selected)


def send_b2(m2):
    mongo.get_collection_pick(m2.selected)
    print(m2.selected)


mongo = Mongo()

scene.caption = "Choose a nest to view: \n"

db_select = menu(index=0, choices=['Pick a database...'], bind=send_b1)

for name in mongo.database_names:
    db_select.choices.append(name)

scene.append_to_caption('    ')

coll_select = menu(index=0, choices=['Pick a collection...'], bind=send_b2)

for i in range(10, 501, 10):
    coll_select.choices.append(str(i))

for i in range(500, 5501, 100):
    coll_select.choices.append(str(i))


def draw_nest():
    global complete, stepwise, last
    count = mongo.collection.count()
    nest = mongo.collection.find_one({'Nest ID': random.randrange(count)})

    print(nest)

    cells = nest["Cells"]
    build_order = nest["Build order"]
    build_height = nest["Build height"]

    complete.delete()
    complete = canvas(width=WIDTH, height=HEIGHT, align='right')

    x_pointer = arrow(canvas=complete, pos=vec(-20, 11.5, 0), axis=vec(40, -23, 0), shaftwidth=0.1, headwidth=0.2, color=color.red)
    y_pointer = arrow(canvas=complete, pos=vec(-20, -11.5, 0), axis=vec(40, 23, 0), shaftwidth=0.1, headwidth=0.2, color=color.green)
    z_pointer = arrow(canvas=complete, pos=vec(0, -20, 0), axis=vec(0, 40, 0), shaftwidth=0.1, headwidth=0.2, color=color.blue)
    w_pointer = arrow(canvas=complete, pos=vec(0, 0, -20), axis=vec(0, 0, 40), shaftwidth=0.1, headwidth=0.2, color=color.white)

    for cell in cells:
        x = cell["Cartesian X"]
        y = cell["Cartesian Y"]
        z = cell["Height"]

        extrusion(canvas=complete, path=[vec(x, y, 0), vec(x, y, z)], shape=[shapes.hexagon(length=0.55, rotate=0.54)],
                  pos=vec(x, y, (z / 2)), color=color.yellow, opacity=0.5)

    stepwise.delete()
    stepwise = canvas(width=WIDTH, height=HEIGHT)

    previous_heights = {}

    index = 0

    # for step in build_order:
    #     try:
    #         last.color = color.yellow
    #         last.opacity = 0.5
    #     except NameError:
    #         print("GUESS WHAT LAST NOT DEFINED")
    #
    #     c = cells[step]
    #     x = c["Cartesian X"]
    #     y = c["Cartesian Y"]
    #
    #     z = build_height[index]
    #
    #     index += 1
    #
    #     old_step = 0
    #
    #     if step in previous_heights:
    #
    #         old_step = previous_heights[step]
    #
    #     # print("{0} {1} {2} {3} {4}".format(c, x, y, z, old_step))
    #
    #     previous_heights[step] = z
    #     z_pos = (z + old_step) / 2
    #
    #     last = extrusion(canvas=stepwise, path=[vec(x, y, old_step), vec(x, y, z)],
    #                      shape=[shapes.hexagon(length=0.55, rotate=0.54)], pos=vec(x, y, z_pos),
    #                      color=color.cyan, opacity=0.75)
    #
    #     sleep(1 / sl.value)


b1 = button(text='Get a nest!', bind=draw_nest)

scene.append_to_caption('\n\n   ')


def set_speed(s):
    wt.text = '{:1.2f}'.format(s.value)


sl = slider(min=1.0, max=10.0, value=4.0, length=220, bind=set_speed, right=15)

wt = wtext(text='{:1.2f}'.format(sl.value))

scene.append_to_caption(' steps/second\n')

complete = canvas(width=0, height=0)

stepwise = canvas(width=0, height=0)
