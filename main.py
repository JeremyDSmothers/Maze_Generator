from math import floor, sqrt
import pygame
from pygame.constants import QUIT
import helper
import random
import colorsys
pygame.init()

#global variables
window_width = window_height = 900
square_width = 20
grid = []
#current cell
current = None

stack = []

# win = pygame.display.set_mode((0, 0), pygame.NOFRAME)

# flags = win.get_flags()
# bits = win.get_bitsize()

# win = pygame.display.set_mode()

# window_width, window_height = pygame.display.get_surface().get_size()

win = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Maze Generator")

clock = pygame.time.Clock()

def calc_dist(v1, v2):
    return floor(sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1]) ** 2))

#classes
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.color = None
                      #t    #r    #b    #l
        self.walls = [True, True, True, True]
        self.visited = False

    def show(self, grid_ind):
        x = self.i * square_width
        y = self.j * square_width

        #fill visited cell with purple alpha color
        if self.visited:
            if(self.color is None):
                currentVect = pygame.math.Vector2(self.i, self.j)

                dist = calc_dist(currentVect, center)
                hu = dist / max_dist

                r, g, b = colorsys.hsv_to_rgb(hu, 1, 1)
                r *= 255
                g *= 255
                b *= 255
                self.color = (r, g, b)

            helper.draw_rect_alpha(win, self.color, (x, y, square_width, square_width))
        
        black = (0, 0, 0)
        #top line
        if self.walls[0]:
            pygame.draw.line(win, black, (x,                y),                (x + square_width, y))
        #right line
        if self.walls[1]:
            pygame.draw.line(win, black, (x + square_width, y),                (x + square_width, y + square_width))
        #bottom line
        if self.walls[2]:
            pygame.draw.line(win, black, (x,                y + square_width), (x + square_width, y + square_width))
        #left line
        if self.walls[3]:
            pygame.draw.line(win, black, (x,                y),                (x,                y + square_width))

    def checkNeighbors(self):
        neighbors = []

        topInd    = index(self.i,     self.j - 1)
        rightInd  = index(self.i + 1, self.j)
        bottomInd = index(self.i,     self.j + 1)
        leftInd   = index(self.i - 1, self.j)

        top = None
        right = None
        bottom = None
        left = None

        if topInd != -1:
            top =    grid[topInd]
        if rightInd != -1:
            right =  grid[rightInd]
        if bottomInd != -1:
            bottom = grid[bottomInd]
        if leftInd != -1:
            left =   grid[leftInd]

        if top is not None and    not(top.visited):
            neighbors.append(top)
        if right is not None and  not(right.visited):
            neighbors.append(right)
        if bottom is not None and not(bottom.visited):
            neighbors.append(bottom)
        if left is not None and   not(left.visited):
            neighbors.append(left)

        if len(neighbors) > 0:
            r = random.randint(0, len(neighbors) - 1)
            return neighbors[r]
        else:
            return None

    def highlight(self):
        x = self.i * square_width
        y = self.j * square_width

        helper.draw_rect_alpha(win, (0, 0, 255, 100), (x, y, square_width, square_width))

##### begin setup "function" #####
cols = window_width // square_width
rows = window_height // square_width

for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)

current = grid[0]
current.highlight()

origin = pygame.math.Vector2(0, 0)
center = pygame.math.Vector2(rows//2, cols//2)
max_dist = calc_dist(origin, center)

##### end setup "function" ######

def reset():
    global grid
    grid = []

    for j in range(rows):
        for i in range(cols):
            cell = Cell(i, j)
            grid.append(cell)
    global current
    current = grid[0]
    current.highlight()

def index(i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return -1

    return i + (j * cols)

def removeWalls(a, b):
    x = a.i - b.i

    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False
    
    y = a.j - b.j
    
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False

def redrawGameWindow():
    win.fill((51, 51, 51))

    for i in range(len(grid)):
        grid[i].show(i)

    global current
    current.visited = True
    current.highlight()
    global firstIter

    #STEP 1
    next = current.checkNeighbors()

    if next is not None:
        next.visited = True

        #STEP 2
        stack.append(current)

        #STEP 3
        removeWalls(current, next)

        #STEP 4
        current = next
    elif len(stack) > 0:
        current = stack.pop()
        current.highlight()
    else:
        reset()

    pygame.display.update()

#main loop
run = True
while run:
    # clock.tick(200)
    # pygame.time.delay(250)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()

pygame.quit()