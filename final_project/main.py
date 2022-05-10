from cmu_graphics import *

# Fill me in!

class SpecialObject(object):
    def __init__(self, w, h, xPos=None, yPos=None, drawing=None):
        self.w = w or 50
        self.h = h or 50
        
        # Prevent the object from going outside of borders
        self.xPos = xPos if xPos is not None else randrange(0 + self.w, 400 - self.w)
        self.yPos = yPos if yPos is not None else randrange(0 + self.h, 400 - self.h)

        self.speedX = 2.5
        self.speedY = 2.5

        self.drawing = drawing
        
        # print(self.xPos, self.yPos, self.w, self.h)

    def draw(self):
        self.drawing = self.drawing

    def distanceTo(self, obj):
        a = (self.xPos - obj.xPos)
        b = (self.yPos - obj.yPos)
        
        distance = (a**2 + b**2) ** 0.5
        
        return a, b, distance

        
    def distanceToObject(self, obj):
        a, b, distance = self.distanceTo(obj)
        a /= distance
        b /= distance

        direction = (a, b)
        
        return direction
        

class Player(SpecialObject):
    def __init__(self, startX=None, startY=None):
        self.xPos, self.yPos = 0, 0
        self.w = 25
        self.h = 25
        
        self.dx = 0
        self.dy = 0
        
        self.dir = [0, 0]
        
        drawing = Group(
                Rect(self.xPos, self.yPos, self.w, self.h, fill="blue")
            )

        super().__init__(self.w, self.h, xPos=startX, yPos=startY, drawing=drawing)

        self.draw()
            
        
            
    def move(self):

        self.xPos += self.speedX * self.dir[0]
        self.yPos += self.speedY * self.dir[1]
        
        if self.xPos>= 400:
            self.xPos = 0 + self.w
        
        elif self.xPos<= 0:
            self.xPos = 400 - self.w
            
        if self.yPos >= 400:
            self.yPos = 0 + self.h
            
        elif self.yPos <= 0:
            self.yPos = 400 - self.h


    
class Enemey(SpecialObject):
    def __init__(self, startX=None, startY=None):
        self.xPos, self.yPos = 0, 0
        self.w = 25
        self.h = 25
        
        # velocity
        self.dx = 1
        self.dy = 1
        
        drawing = Group(
            Rect(self.xPos, self.yPos, self.w, self.h, fill="red")
            )

        super().__init__(self.w, self.h, xPos=startX, yPos=startY, drawing=drawing)
        
        self.draw()
        
    
    def move(self, distRef, enemies):

        distX, distY = self.distanceToObject(distRef)

        # add when hitting corner change dir to the player position
        if self.xPos + self.w >= 400:
            self.speedX *= -1
        
        elif self.xPos - self.w <= 0:
            self.speedX *= -1
            
        if self.yPos + self.h >= 400:
            self.speedY *= -1
            
        elif self.yPos - self.h <= 0:
            self.speedY *= -1


        # make sure not to collide with other enemies
        for enemy in enemies:
            if enemy.drawing != self.drawing:
                x, y, _ = self.distanceTo(enemy)

                if enemy.drawing.hitsShape(self.drawing):
                    self.xPos += x
                    self.yPos += y

        self.xPos += self.speedX * distX
        self.yPos += self.speedY * distY

        self.draw()

        print(self.xPos, self.yPos)

def onKeyHold(keys):
    if "W" in keys or "w" in keys:
        app.player.dir[1] = -1

    if "D" in keys or "d" in keys:
        app.player.dir[0] = 1

    if "S" in keys or "s" in keys:
        app.player.dir[1] = 1

    if "A" in keys or "a" in keys:
        app.player.dir[0] = -1

def onStep():
    
    # app.player.drawing.toFront()

    for enemy in app.enemies:
        
        enemy.move(app.player, app.enemies)

    app.player.move()
        

def main():
    app.player = Player(200, 200)
    
    app.enemies = [Enemey(), Enemey()]

main()

cmu_graphics.run()