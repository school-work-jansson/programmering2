from cmu_graphics import *

# Fill me in!

class SpecialObject(object):
    def __init__(self, w=None, h=None, xPos=None, yPos=None, drawing=None):
        
        self.w = w if w is not None else 25
        self.h = h if h is not None else 25
        
        # Prevent the object from going outside of borders
        self.xPos = xPos if xPos is not None else randrange(0 + self.w, 400 - self.w)
        self.yPos = yPos if yPos is not None else randrange(0 + self.h, 400 - self.h)

        self.speedX = 2.5
        self.speedY = 2.5

        self.drawing = drawing


    def update(self):
        # Update screen
        self.drawing.centerX = self.xPos
        self.drawing.centerY = self.yPos


    def distanceTo(self, obj):
        # Using pythagorean theorem to calculate the distance between two objects
        x = (self.xPos - obj.xPos)
        y = (self.yPos - obj.yPos)
        
        distance = (x**2 + y**2) ** 0.5
        
        return x, y, distance
        
        
    def directionToObject(self, obj):
        # Calculating the direction to a object 
        # Used to move enemey towards player
        # ref: https://stackoverflow.com/questions/2625021/game-enemy-move-towards-player

        x, y, distance = self.distanceTo(obj)
        x /= distance
        y /= distance

        direction = (x, y)
        
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

        self.update()
            
        
            
    def move(self):
        # Move player towards self.direction
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

        self.update()


    
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
        
        self.update()
        
    
    def move(self, distRef, enemies):

        distX, distY = self.directionToObject(distRef)

        # Corner colission
        if self.xPos > 400 - self.w:
            self.speedX *= -1
        
        elif self.xPos < 0 + self.w:
            self.speedX *= -1
            
        if self.yPos  > 400 - self.h:
            self.speedY *= -1
            
        elif self.yPos  < 0 + self.h:
            self.speedY *= -1

        self.xPos += self.speedX * distX
        self.yPos += self.speedY * distY

        # make sure not to collide with other enemies
        # Works but is buggy
        for enemy in enemies:
            if enemy.drawing != self.drawing:
                x_dist, y_dist, _ = self.distanceTo(enemy)

                while enemy.drawing.hitsShape(self.drawing):
                    self.xPos += x_dist
                    self.yPos += y_dist
            
                    self.update()
                
                # Print distance between the enemy
                # print(x_dist, y_dist)

        self.update()


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


# Initial start create player instance and enemies
def main():
    app.player = Player(200, 200)
    app.enemies = []

    for i in range(2):
        app.enemies.append(Enemey())

main()

cmu_graphics.run()