# Class
from cmu_graphics import *

class Grid:
    def __init__(self):
        print("Initilization of Grid")
        
        self.drawing = []
        self.currentActive = None
        self.gridSize = 25
        self.currentActiveRow = 0
        self.currentActiveCol = 0
        
        self.createGrid()

        self.gameOver = False
        self.gameOverLabel = Label("Game Over.", 200, 200, size=50, fill=None)
        self.score = Label(0, 350, 50, fill="white", size=50)
        
        self.title = Group(
            Rect(25, 175, 350, 75),
            Label("Slow phased game.", 200, 200, size=25, fill="gold"),
            Label("Try to avoid the red square using the arrow keys.", 200, 224, size=15, fill="gold"),
        )
        
    
    def createGrid(self):
        print("Drawing Grid")
        # Loop
        for row in range(0, 400, self.gridSize):
            rad = []
            for col in range(0, 400, self.gridSize):
                box = Rect(row, col, row + self.gridSize, col + self.gridSize, fill="grey", border=None, borderWidth=1)
                rad.append(box)
        
            self.drawing.append(rad)
        
        
class SpecialRect(object):
    def __init__(self, startX, startY, color):
        # list
        self.position = [startX, startY]
        self.size = 25
        self.color = color
        
        self.drawing = Rect(self.position[0], self.position[1], self.size, self.size, fill=self.color, border="white", borderWidth=1)
    
    def redraw(self):
        app.group.remove(self.drawing)    
        self.drawing = Rect(self.position[0], self.position[1], self.size, self.size, fill=self.color, border="white", borderWidth=1)
    
    def getPos(self):
        return self.position
        
    def getDrawing(self):
        return self.drawing

    
class MovableRect(SpecialRect):
    def __init__(self, startX, startY, color):
        super().__init__(startX, startY, color)
    
    def changePosition(self, x, y):
        # Move the position by a constant "size" in x or y direction
        self.position[0] += x * self.size
        self.position[1] += y * self.size

    def moveObject(self, key):

        if key == "right":
            # Checking for colission with the wall
            if self.drawing.right >= 400:
                self.position[0] = 0
            else:
                # Move Right
                self.changePosition(1, 0)
            
        if key == "left":
            # Checking for colission with the wall
            if self.drawing.left <= 0:
                self.position[0] = 400 - self.size
            else:    
                # Move Left
                self.changePosition(-1, 0)
                
        if key == "up":
            # Checking for colission with the wall
            if self.drawing.top <= 0:
                self.position[1] = 400 - self.size
            else:
                # Move Up
                self.changePosition(0, -1)
                
        if key == "down":
            # Checking for colission with the wall
            if self.drawing.bottom >= 400:
                self.position[1] = 0
            else:
                # Move Down
                self.changePosition(0, 1)
        
        self.redraw()


class Player(MovableRect):
    def __init__(self, startX, startY, color):
        super().__init__(startX, startY, color)
    
    def move(self, key):
        self.moveObject(key)


class Enemey(MovableRect):
    def __init__(self, startX, startY, color):
        super().__init__(startX, startY, color)
        
    def move(self, playerPos):
        dist = self.calculateDistanceToPlayer(playerPos)
        
        if dist[0] > 0:
            self.changePosition(-1, 0)
        
        if dist[0] < 0:
            self.changePosition(1, 0)
            
        if dist[1] > 1:
            self.changePosition(0, -1)
        
        if dist[1] < 1:
            self.changePosition(0, 1)
        
        self.redraw()
            
    
    def calculateDistanceToPlayer(self, playerPos):
        dist = []
        for cord in range(len(self.position)):
            dist.append((self.position[cord] - playerPos[cord]))
        return dist
        
class Objective(SpecialRect):       
    def __init__(self):
        super().__init__(50, 50, "gold" )
        self.newPos()
        self.redraw()
        
    def newPos(self):
        self.position = [randrange(0, 400, self.size), randrange(0, 400, self.size)]
        self.redraw()
    
        
def onKeyPress(key):
    # If the enemy touches the player show the game over score
    if app.enemey.getPos() == app.player.getPos():
        app.grid.gameOverLabel.fill = "red"
        return 
    
    app.grid.title.fill = None

    # If objective position is the same as player position increment the score and move the objective
    if app.objective.getPos() == app.player.getPos():
        app.grid.score.value += 1
        app.objective.newPos()
    
    # Move the player and the enemey
    app.player.move(key)
    app.enemey.move(app.player.position)
 
def main():
    
    app.grid = Grid()
    app.objective = Objective()
    app.player = Player(0,    0, "blue")
    app.enemey = Enemey(350, 350, "red")

main()

cmu_graphics.run()