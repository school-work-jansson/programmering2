# Creating on Github
# github.com/school-work-jansson/programmering2
from cmu_graphics import *

app.background = "black"
Label("CODE IS ON GITHUB", 200, 200, size=25, fill="red", bold=True)

class SpecialCircle():
    def __init__(self):
        self.xPos, self.yPos = randrange(1, 400), 0 
        self.r = randrange(1, 10)
        self.dx, self.dy = 1, randrange(1, 100) / 100   
        self.opacity = randrange(0, 75)
        
        self.drawing = Circle(self.xPos, self.yPos, self.r, opacity=self.opacity, fill="white")
    
    def move(self):
        if self.drawing.centerY >= 400:
            self.drawing.centerY = 0
            self.dy = randrange(1, 100) / 100
        else:
            self.drawing.centerY += self.dy

app.circles = []

def onStep():
    for circle in app.circles:
        circle.move()
    
def main():
    for i in range(500):
        app.circles.append(SpecialCircle())
    

main()

cmu_graphics.run()

