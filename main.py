from math import floor, sqrt
import pygame
from pygame.constants import QUIT
import helper
import random
import colorsys
pygame.init()

clock = pygame.time.Clock()


#future ideas
#DPS at the end of maze generation along with animation
#BFS at the end of maze generation along with animation
#A* search at the end of maze generation along with animation

#global variables
window_width = window_height = 700
square_width = 20
cols = window_width // square_width
rows = window_height // square_width
grid = []
#current cell
current = None

#a star variables
a_grid = []
openSet = []
closedSet = []
start = None
end = None
path = []

a_star = False

stack = []

# win = pygame.display.set_mode((0, 0), pygame.NOFRAME)

# flags = win.get_flags()
# bits = win.get_bitsize()

# win = pygame.display.set_mode()

# window_width, window_height = pygame.display.get_surface().get_size()

win = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Maze Generator")

# clock = pygame.time.Clock()

def calc_dist(v1, v2):
    return floor(sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1]) ** 2))

    
def index(i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return -1

    return i + (j * cols)


#classes
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j

        #a star properties#
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None

        self.color = None
                      #t    #r    #b    #l
        self.walls = [True, True, True, True]
        self.visited = False

    def set_color(self, c):
        self.color = c

    def show(self, param_color):
        x = self.i * square_width
        y = self.j * square_width

        #fill visited cell with purple alpha color
        if self.visited:
            # if(self.color is None):
                # print(param_color)
            self.color = param_color

                ### FOR RAINBOW COLORING ###
                # currentVect = pygame.math.Vector2(self.i, self.j)

                # dist = calc_dist(currentVect, center)
                # hu = dist / max_dist


                # r, g, b = colorsys.hsv_to_rgb(hu, 1, 1)
                # r *= 255
                # g *= 255
                # b *= 255
                # self.color = (r, g, b)

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

    def addNeighbors(self):
        topInd = -1
        rightInd = -1
        bottomInd = -1
        leftInd = -1

        # if(self.i == 0 and self.j == 0):
        #     print(self.walls[0], self.walls[1], self.walls[2], self.walls[3])

        if not(self.walls[0]):
            topInd    = index(self.i,     self.j - 1)
        if not(self.walls[1]):
            rightInd  = index(self.i + 1, self.j)
        if not(self.walls[2]):
            bottomInd = index(self.i,     self.j + 1)
        if not(self.walls[3]):
            leftInd   = index(self.i - 1, self.j)

        # if(self.i == 0 and self.j == 0):
        #     print(topInd, rightInd, bottomInd, leftInd)

        top = None
        right = None
        bottom = None
        left = None

        if topInd != -1:
            top =    grid[topInd]
            self.neighbors.append(top)
        if rightInd != -1:
            right =  grid[rightInd]
            self.neighbors.append(right)
        if bottomInd != -1:
            bottom = grid[bottomInd]
            self.neighbors.append(bottom)
        if leftInd != -1:
            left =   grid[leftInd]
            self.neighbors.append(left)

        # if(self.i == 0 and self.j == 0):
        #     print()


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
a_row = []
a_col = []
for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)
        a_row.append(cell)
    a_grid.append(a_row)
    a_row = []

current = grid[0]
current.highlight()

origin = pygame.math.Vector2(0, 0)
center = pygame.math.Vector2(rows//2, cols//2)
max_dist = calc_dist(origin, center)

start = grid[0]
end = a_grid[rows-1][cols-1]

start.set_color((0, 0, 0))
end.set_color((0, 0, 0))

openSet.append(start)
display_grid_colors = True

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

def remove_from_arr(arr, obj):
    if obj in arr:
        arr.remove(obj)

    return arr

def redrawGameWindow():
    win.fill((51, 51, 51))

    for i in range(len(grid)):
        grid[i].show((255, 255, 255))

    global current
    current.visited = True
    current.highlight()
    global firstIter

    global a_star

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
    elif not(a_star):
        a_star = True


    for i in range(len(closedSet)):
        # print('closedSet show')
        closedSet[i].show((255, 0, 0))

    for i in range(len(openSet)):
        # print('openSet show')
        openSet[i].show((255, 255, 0))

    for i in range(len(path)):
        # print('path show')
        path[i].show((0, 0, 255))

    pygame.display.update()

def heuristic(a,b):
    operand_1 = a.i - b.i
    operand_2 = a.j - b.j

    left = operand_1 * operand_1
    right = operand_2 * operand_2

    under_sqrt = left + right

    return sqrt(under_sqrt)
    

def a_star_loop():    
    global openSet
    # print(len(grid[0].neighbors))
    if len(openSet) > 0:
        #keep going
        
        winner = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[winner].f:
                winner = i
        current = openSet[winner]


        if current == end:
            #find the best path

            print('DONE!')
            global path
            path = []
            temp = current
            path.append(temp)
            while temp.previous is not None:
                path.append(temp.previous)
                temp = temp.previous

        # print(len(openSet))
        openSet = remove_from_arr(openSet, current)
        # print(len(openSet))
        # closedSet.append(current)

        # print(current.i, current.j)
        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            # print(neighbor.i, neighbor.j)

            if neighbor not in closedSet:
                temp_g = current.g + 1

                if neighbor in openSet:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                else:
                    # print(neighbor.g)
                    neighbor.g = temp_g
                    openSet.append(neighbor)
            
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.previous = current

    else:
        #no solution
        print('meh2')

    pygame.display.update()

    

#main loop
run = True
pause = False
need_neighbors = True
while run:
    # pygame.time.wait(500)
    # clock.tick(2)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        print('pause')
        pause = not(pause)

    if not(pause):
        # clock.tick(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redrawGameWindow()
        if a_star:

            #instantiate neighbors from constructed maze
            if need_neighbors:
                need_neighbors = False
                for i in range(len(grid)):
                    grid[i].addNeighbors()

            a_star_loop()

pygame.quit()