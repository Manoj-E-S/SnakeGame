import sys
import pygame
from pygame.locals import *
from tkinter import *
from tkinter import messagebox
import random
import math

pygame.init()

################################################################## CLASSES ##########################################################################

class Cube():
    
    rows = 20
    width = 600

    def __init__(self, pos, color, dirnx=0, dirny=-1):
        self.pos = pos          # pos = Grid co-ordinate system tuple
        self.dirnx = dirnx      # move along a row
        self.dirny = dirny      # move long a column
        self.color = color      # cube fill color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        boxSide = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*boxSide + 1, j*boxSide + 1, boxSide - 1, boxSide - 1))
        
        if eyes:
            centreCube = boxSide // 2
            radius = 3
            centre1 = (i*boxSide + centreCube - 7, j*boxSide + 8)
            centre2 = (i*boxSide + centreCube + 7, j*boxSide + 8)
            pygame.draw.circle(surface, (0, 0, 0), centre1, radius)
            pygame.draw.circle(surface, (0, 0, 0), centre2, radius)

#_____________________________________________________________________________________________________________________________________________________

class Snake():

    body = []       # list of Cubes
    turns = {}      # (dirnx, dirny) such that 1, -1, 0 for each of dirnx and dirny
    points = 0

    def __init__(self, color, pos):
        '''
        Initially snake moves upward
        '''
        self.color = color                                                                  # Snake color
        self.head = self.tail = Cube(pos, dirnx=0, dirny=-1, color=self.color)              # Snake head (has eyes) is also its tail initially
        self.body.append(self.head)                                                         # list of Cubes


    def move(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.head.dirnx = -1
                self.head.dirny = 0
                self.turns[self.head.pos] = (self.head.dirnx, self.head.dirny)
            elif keys[pygame.K_RIGHT]:
                self.head.dirnx = 1
                self.head.dirny = 0
                self.turns[self.head.pos] = (self.head.dirnx, self.head.dirny)
            elif keys[pygame.K_UP]:
                self.head.dirnx = 0
                self.head.dirny = -1
                self.turns[self.head.pos] = (self.head.dirnx, self.head.dirny)
            elif keys[pygame.K_DOWN]:
                self.head.dirnx = 0
                self.head.dirny = 1
                self.turns[self.head.pos] = (self.head.dirnx, self.head.dirny)
        
        for i, cube in enumerate(self.body):
            position = cube.pos
            if position in self.turns:
                turn = self.turns[position]
                cube.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(position)
            else:
                if cube.dirnx == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows - 1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows - 1:
                    cube.pos = (0, cube.pos[1])
                elif cube.dirny == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows - 1)
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows - 1:
                    cube.pos = (cube.pos[0], 0)
                else:
                    cube.move(cube.dirnx, cube.dirny)


    def reset(self, pos):
        
        response = messagebox.askquestion("GAME OVER", f"SCORE: {self.points}\nDo you want to try again?")
        if response == "yes":
            self.body = []
            self.turns = {}
            self.head = self.tail = Cube(pos, color=self.color)
            self.body.append(self.head)
        else:
            pygame.display.quit()
            pygame.quit()
            sys.exit()


    def addCube(self):
        
        self.tail = Cube((self.tail.pos[0] - self.tail.dirnx, self.tail.pos[1] - self.tail.dirny), dirnx=self.tail.dirnx, dirny=self.tail.dirny, color=self.color)
        self.body.append(self.tail)
        self.points += 1


    def draw(self, surface):
        
        for i, cube in enumerate(self.body):
            if i == 0:
                cube.draw(surface, eyes=True)
            else:
                cube.draw(surface, eyes=False)


####################################################################################################################################################################

################################################################################# UTILS ############################################################################

def generateFood(snake):

    global rows, snack_col

    body_copy = snake.body
    check = True
    while check:
        food_pos = (random.randrange(0, rows), random.randrange(0, rows))
        if len(list(filter(lambda cube: cube.pos == food_pos, body_copy))) > 0:
            check = True
        else:
            check = False

    food = Cube(pos=food_pos, color=snack_col)
    return food

#__________________________________________________________________________________________________________________________________________________________________

def drawGrid(surface, rows, width):
    
    boxSide = width // rows

    x = 0
    y = 0
    for _ in range(rows):
        x = x + boxSide
        y = y + boxSide
        pygame.draw.line(surface, (20, 20, 20), (x, 0), (x, width))
        pygame.draw.line(surface, (20, 20, 20), (0, y), (width, y))

#__________________________________________________________________________________________________________________________________________________________________

def redrawWindow(surface):
    
    global width, rows, s, food
    surface.fill((0, 0, 0))

    drawGrid(surface, rows, width)
    s.draw(surface)
    food.draw(surface)
    pygame.display.update()

#_________________________________________________________________________________________________________________________________________________________________

def Launch(window, snake_color, snack_color):

    global snake_col, snack_col, win, width
    snake_col = tuple([int(x) for x in snake_color.get().strip('(').strip(')').split(', ')])
    snack_col = tuple([int(x) for x in snack_color.get().strip('(').strip(')').split(', ')])

    window.destroy()

    win = pygame.display.set_mode((width, width), flags=pygame.SHOWN)
    pygame.display.set_caption("Snake Game")

    global s, food

    s = Snake(color=snake_col, pos=(10, 10))
    food = generateFood(s)

#_________________________________________________________________________________________________________________________________________________________________

def openingWindow():

    root = Tk()
    root.title("Snake Game Preferences")
    # root.geometry("800x800")

    Label(root, text="The Snake Game", font=("Merriweather", 50), anchor="center").grid(row=0, column=0, columnspan=2, sticky=W+E, pady=(30, 10))

    snake_color_lab = Label(root, text="Snake Color (R, G, B): ", anchor="center", font=("Helvetica", 20))
    snake_color = Entry(root)
    snake_color_lab.grid(row=1, column=0, padx=(100, 20))
    snake_color.grid(row=1, column=1, sticky=W+E, padx=(20, 100))

    snack_color_lab = Label(root, text="Snack Color (R, G, B): ", anchor="center", font=("Helvetica", 20))
    snack_color = Entry(root)
    snack_color_lab.grid(row=2, column=0, padx=(100, 20))
    snack_color.grid(row=2, column=1, sticky=W+E, padx=(20, 100))

    launch = Button(root, text="Launch", command=lambda: Launch(root, snake_color, snack_color))
    launch.grid(row=3, column=0, columnspan=2, ipadx=250, ipady=10, padx=100, pady=(5, 50))

    root.mainloop()


###################################################################################################################################################################


# MAIN Function

def main():

    global width, rows, s, food, win
    width = 600 # Equal width and height
    rows = 20   # Equal no. of rows and columns
 
    openingWindow()

    run = True
    clock = pygame.time.Clock()
    while run:
        # pygame.time.delay(150)  # 150ms delay the loop (Slows the execution)
        clock.tick(8)          # Max 10fps: snake can move max 10 blocks per second (Speeds up the execution)

        redrawWindow(win)
        
        s.move()
        
        if s.head.pos == food.pos:
            food = generateFood(s)
            s.addCube()

        for x in s.body:
            if x is not s.head and x.pos == s.head.pos:
                s.reset((15, 15))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

##################################################################################################################################################################


