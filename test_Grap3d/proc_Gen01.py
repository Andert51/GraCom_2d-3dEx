from tkinter import *
import random as rand

# Initialize the root window and canvas
root = Tk()
root.title("Terrain Visualization")
resX = 1000
resY = 500
canvas = Canvas(root, bg="blue", height=resY, width=resX)
canvas.pack()

# Map configuration
map = {
    'xy': [200, 100],  # Grid size
    'cLevel': 0,       # Sea level
    'nodes': [],
    'seed': 10,        # Seeding probability
    'Choice': [-100, 200]  # Elevation/temperature choices
}

# Node class representing each grid cell
class Node:
    def __init__(self, xy):
        self.xy = xy
        self.el = 0
        self.temp = 0
        self.neighbors = []
        self.active = True

    def render(self):
        # Determine color based on elevation and temperature
        if self.el <= -25:
            color = 'dark blue'
        elif self.el <= map['cLevel']:
            color = 'blue'
        elif self.el <= 25 and self.temp <= 0:
            color = 'light grey'
        elif self.el <= 25 and self.temp <= 5:
            color = 'green'
        elif self.el <= 25 and self.temp <= 10:
            color = 'dark green'
        elif self.el <= 25 and self.temp <= 100:
            color = 'yellow'
        else:
            color = 'white'

        # Draw the node as a rectangle
        a = self.xy[0] * 5
        b = self.xy[1] * 5
        c = a + 5
        d = b + 5
        canvas.create_rectangle(a, b, c, d, fill=color, outline=color)

# Generate nodes for the map
def genNodes():
    for i in range(map['xy'][0]):
        for j in range(map['xy'][1]):
            map['nodes'].append(Node([i, j]))
    print("Nodes generated.")

# Calculate neighbors for each node
def getNeighbors():
    node_dict = {(n.xy[0], n.xy[1]): n for n in map['nodes']}
    for n in map['nodes']:
        x, y = n.xy
        neighbors = [
            node_dict.get((x - 1, y)),
            node_dict.get((x + 1, y)),
            node_dict.get((x, y - 1)),
            node_dict.get((x, y + 1))
        ]
        n.neighbors = [neighbor for neighbor in neighbors if neighbor]
    print("Neighbors calculated.")

# Seed the map with random elevation and temperature
def seed():
    for n in map['nodes']:
        if 40 < n.xy[0] < 160 and 20 < n.xy[1] < 80:
            if rand.randint(0, 1000) <= map['seed']:
                n.el = rand.choice(map['Choice'])
                n.temp = rand.choice(map['Choice'])
    print("Map seeded.")

# Set all nodes to active
def setActive():
    for n in map['nodes']:
        n.active = True

# Smooth the map by averaging elevation and temperature with neighbors
def smoothMap():
    for n1 in map['nodes']:
        n1.active = False
        for n2 in n1.neighbors:
            if n2.active:
                if n1.el != n2.el:
                    if rand.randrange(0, 100) < 5:
                        avg_el = (n1.el + n2.el) / 2
                        n1.el = avg_el
                        n2.el = avg_el
                    if rand.randrange(0, 100) < 5:
                        avg_temp = (n1.temp + n2.temp) / 2
                        n1.temp = avg_temp
                        n2.temp = avg_temp

# Raise land elevation
def raiseLand():
    for n in map['nodes']:
        if n.el > 0 and rand.randrange(0, 100) < 1:
            n.el += 100

# Lower sea level
def lowerSea():
    for n in map['nodes']:
        if n.el <= 0 and rand.randrange(0, 100) < 1:
            n.el -= 100

# Raise temperature
def raiseTemp():
    for n in map['nodes']:
        if n.el > 0 and rand.randrange(0, 100) < 1:
            n.temp += 10

# Cool down temperature
def coolTemp():
    for n in map['nodes']:
        if n.temp > 0 and rand.randrange(0, 100) < 1:
            n.temp -= 10

# Erode land
def erodeLand():
    for n in map['nodes']:
        if n.el > 0 and rand.randrange(0, 100) < 1:
            n.el -= 50

# Render the entire map
def renderMap():
    canvas.delete("all")
    for n in map['nodes']:
        n.render()
    drawLegend()
    canvas.update()

# Draw a legend for the visualization
def drawLegend():
    legend_items = [
        ("Dark Blue", "Deep Water"),
        ("Blue", "Shallow Water"),
        ("Light Grey", "Beach"),
        ("Green", "Lowland"),
        ("Dark Green", "Forest"),
        ("Yellow", "Desert"),
        ("White", "Snow")
    ]
    x, y = 10, 10
    for color, label in legend_items:
        canvas.create_rectangle(x, y, x + 20, y + 20, fill=color, outline=color)
        canvas.create_text(x + 30, y + 10, anchor="w", text=label, fill="white")
        y += 30

# Interactive processes
def process1():
    setActive()
    smoothMap()
    renderMap()

def process2():
    setActive()
    lowerSea()
    renderMap()

def process3():
    setActive()
    raiseLand()
    renderMap()

def process4():
    setActive()
    raiseTemp()
    renderMap()

def process5():
    setActive()
    coolTemp()
    renderMap()

def process6():
    setActive()
    erodeLand()
    renderMap()

# Add interactive buttons
def addButtons():
    button_frame = Frame(root)
    button_frame.pack()
    Button(button_frame, text="Smooth", command=process1).pack(side=LEFT)
    Button(button_frame, text="Lower Sea", command=process2).pack(side=LEFT)
    Button(button_frame, text="Raise Land", command=process3).pack(side=LEFT)
    Button(button_frame, text="Heat", command=process4).pack(side=LEFT)
    Button(button_frame, text="Cool", command=process5).pack(side=LEFT)
    Button(button_frame, text="Erode", command=process6).pack(side=LEFT)

# Initialize the map
genNodes()
getNeighbors()
seed()
renderMap()
addButtons()

# Start the Tkinter main loop
mainloop()