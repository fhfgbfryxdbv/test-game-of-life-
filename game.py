#бібліотеки
import pygame
import random
import copy

pygame.init()
pygame.display.set_caption("Game of Life")
gui_font = pygame.font.Font(None, 20)

#параметри вікна
Width, Height = 550, 610
Screen = pygame.display.set_mode((Width, Height))

class Button():
    def __init__(self, x, y, text="", width = 60, height = 35):

        #параметри кнопки
        self.pressed=False
        self.elevation = 6
        self.dynamicElevation = self.elevation
        self.originalYpos = y

        #параметри прямокутників
        self.top_rect = pygame.Rect((x, y), (width, height))
        self.top_colour = '#CCCCCC'

        self.bottom_rect = pygame.Rect((x, y), (width, height))
        self.bottom_colour ="#AAAAAA" 

        #параметри тексту
        self.text = gui_font.render(text, True, "#000000")
        self.text_rect = self.text.get_rect(center = self.top_rect.center)

    def draw(self):
        self.top_rect.y = self.originalYpos - self.dynamicElevation
        self.text_rect.center = self.top_rect.center

        pygame.draw.rect(Screen, self.bottom_colour, self.bottom_rect, border_radius=6)
        pygame.draw.rect(Screen, self.top_colour, self.top_rect, border_radius=6)
        Screen.blit(self.text, self.text_rect)
    
    def clickCheck(self, func, args):

        pos = pygame.mouse.get_pos()

        if self.top_rect.collidepoint(pos):
            self.top_colour ='#FFFFFF'

            if pygame.mouse.get_pressed()[0]:
                self.dynamicElevation=0
                self.pressed = True

            else:
                self.dynamicElevation=self.elevation

                if self.pressed == True:
                    func(*args)
                    self.pressed = False

        else:
            self.dynamicElevation=self.elevation
            self.top_colour='#CCCCCC'

class label():
    def __init__(self, x, y, name="", width = 60, height = 35):
        self.rect = pygame.Rect((x, y), (width, height))
        self.colour = '#FFFFFF'

        self.name =  gui_font.render(name, True, "#000000")
        self.name_rect = self.name.get_rect(center = pygame.Rect((x, y-25), (width, height)).center)
    
    def draw(self, parametr):
        self.parametr = gui_font.render(f"{parametr}", True, "#000000")
        self.parametr_rect = self.parametr.get_rect(center = self.rect.center)
 
        pygame.draw.rect(Screen, self.colour, self.rect)
        for i in range (2):
            pygame.draw.line(Screen, 0, (self.rect.x, self.rect.y+(i*self.rect.height)), (self.rect.x+self.rect.width, self.rect.y+(i*self.rect.height)), 4)
            pygame.draw.line(Screen, 0, (self.rect.x+(i*self.rect.width), self.rect.y), (self.rect.x+(i*self.rect.width), self.rect.y+self.rect.height), 4)
        Screen.blit(self.name, self.name_rect)
        Screen.blit(self.parametr, self.parametr_rect)

#Функції

def Pause():
    global Paused
    if Paused == False:
        Paused = True
    else: 
         Paused = False

def recoverGrid():
    global Grid, temp
    Grid = copy.deepcopy(originalGrid)
    temp = copy.deepcopy(originalGrid)
         

def generateGrid():
    global originalGrid, Grid, temp
    originalGrid = [[random.choice(types) for i in range(gridSize)] for j in range(gridSize)]
    Grid = copy.deepcopy(originalGrid) #створюємо копію першочергової сітки
    temp = copy.deepcopy(originalGrid)  #створюємо ще тимчасовий двовимірний масив

def clearGrid():
    global Grid, temp
    Grid = [[ dead for i in range(gridSize)] for j in range(gridSize)]
    temp = copy.deepcopy(Grid)

def SpeedUp():
    global FPS
    if FPS>=10 and FPS<=50:
        FPS+=5
        print(FPS)
    else:
        print("speed limit")
        FPS-=10
        
def SlowDown():
    global FPS
    if FPS>=10 and FPS<=50:
        FPS-=5
        print(FPS)
    else:
        print("speed limit")
        FPS+=5
                    
def drawGrid(grid,size):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            pygame.draw.rect(Screen, cell, (j*pixelSize, i*pixelSize, pixelSize, pixelSize))
    for i in range(size+1):
        pygame.draw.line(Screen, 0, (i*pixelSize, 0), (i*pixelSize, gridSize*pixelSize))
        pygame.draw.line(Screen, 0, (0, i*pixelSize), (gridSize*10, i*pixelSize))

def rulesOfNature(grid, tempGrid):
    global population
    if Paused == False:
        population = 0
        for  i in range(len(grid)):
            for j in range(len(grid)):
                det=int(grid[(i-1)%gridSize][(j-1)%gridSize]==alive)+int(grid[(i-1)%gridSize][j]==alive)+int(grid[(i-1)%gridSize][(j+1)%gridSize]==alive)+int(grid[i][(j-1)%gridSize]==alive)+int(grid[i][(j+1)%gridSize]==alive)+int(grid[(i+1)%gridSize][(j-1)%gridSize]==alive)+int(grid[(i+1)%gridSize][j]==alive)+int(grid[(i+1)%gridSize][(j+1)%gridSize]==alive)
                if grid[i][j] == alive:
                    if (det<2) or (det>3):
                        tempGrid[i][j] = types[1]
                    population+=1
                elif grid[i][j] == dead:
                    if det == 3:
                        tempGrid[i][j] = types[0]
                        population+=1

    return copy.deepcopy(tempGrid)

def draw(grid):
    x,y = pygame.mouse.get_pos() #отримуємо озицію курсору
    Pressed=True
    if x >= 0 and x <= Width and y >= 0 and y <= Width:
        x = x//pixelSize
        y = y//pixelSize
        if Pressed==True:
            if grid[y][x]==dead:
                grid[y][x]=alive
            else:
                grid[y][x]=dead
            Pressed=False
    
    
#атрибути
pixelSize = 10 #розмір клітинки
gridSize = 55  #розмір ігрового поля
Paused = False

alive,dead ='#C3C3C3', '#000000'  #вибір кольору клітини
types=[alive,dead]
population=0

FPS = 30  #Швидкість гри
speed = pygame.time.Clock()

generateGrid()

#кнопки
pauseButton=Button(5, 565, "Pause")
clearButton=Button(70, 565, "Clear")
generationButton=Button(135, 565, "Regenerate", width=80)
recoveringButton=Button(220, 565, "Recover")
speedUp = Button(285, 565, "Speed Up")
slowDown = Button(350, 565, "Slow Down", width=80)

#оголошення label
populationLabel=label(455, 570, "популяція")
                     
run = True
while run:
    Screen.fill("#81E1FF")
    pauseButton.draw()
    clearButton.draw()
    generationButton.draw()
    recoveringButton.draw() 
    slowDown.draw()
    speedUp.draw()
    populationLabel.draw(population)
    speed.tick(FPS)
    for event in pygame.event.get():
        pauseButton.clickCheck(Pause, ())
        clearButton.clickCheck(clearGrid, ())
        generationButton.clickCheck(generateGrid, ())
        recoveringButton.clickCheck(recoverGrid, ())
        speedUp.clickCheck(SpeedUp, ())
        slowDown.clickCheck(SlowDown, ())
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
        if pygame.mouse.get_pressed()[0]:
            draw(temp)
         
    drawGrid(Grid,gridSize)
    Grid = rulesOfNature(Grid, temp)
    pygame.display.update()
