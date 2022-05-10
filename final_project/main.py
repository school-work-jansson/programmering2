from cmu_graphics import *
import time
# Fill me in!



class SpecialObject(object):
    def __init__(self, w=None, h=None, xPos=None, yPos=None, drawing=None):
        
        self.w = w if w is not None else 25
        self.h = h if h is not None else 25
        
        # Prevent the object from going outside of borders
        self.xPos = xPos if xPos is not None else randrange(0 + self.w, 400 - self.w)
        self.yPos = yPos if yPos is not None else randrange(0 + self.h, 400 - self.h)

        self.speedX = 1.5
        self.speedY = 1.5

        self.drawing = drawing

        self.angle = 0


    def update(self):
        # Update screen
        self.drawing.centerX = self.xPos
        self.drawing.centerY = self.yPos
        self.drawing.rotateAngle = self.angle


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


class Objective(SpecialObject):
    def __init__(self):
        self.xPos = randrange(0, 400)
        self.yPos = randrange(0, 400)
        self.r = 12.5

        drawing = Group(
            Star(self.xPos, self.yPos, self.r, 5, fill="gold")
        )
        
        super().__init__(drawing=drawing)

        self.update()
    
    def newPos(self):
        self.xPos = randrange(0, 400)
        self.yPos = randrange(0, 400)

        self.update()


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

        self.speedX = 2.5
        self.speedY = 2.5
            
        
            
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
        self.last_hit = time.time()
        
        drawing = Group(
            Rect(self.xPos, self.yPos, self.w, self.h, fill="red", border="darkred", )
            )

        super().__init__(self.w, self.h, xPos=startX, yPos=startY, drawing=drawing)
        
        self.update()
        
    
    def move(self, distRef, enemies):

        distX, distY = self.directionToObject(distRef)
        self.angle += 5


        # Corner colission
        if self.xPos > 400 - self.w:
            self.speedX *= -1
            self.angle += 45
        
        elif self.xPos < 0 + self.w:
            self.speedX *= -1
            self.angle += 45
            
        if self.yPos  > 400 - self.h:
            self.speedY *= -1
            self.angle += 45
            
        elif self.yPos  < 0 + self.h:
            self.speedY *= -1
            self.angle += 45



        
        # make sure not to collide with other enemies
        # Works but is buggy
        for enemy in enemies:
            # Dont check for it self
            if enemy.drawing != self.drawing:
                if enemy.drawing.hitsShape(self.drawing):
                    self.speedY *= -1
                    self.speedX *= -1

                    self.xPos += self.speedX + 1
                    self.yPos += self.speedY + 1

                    self.update()

                    # Add delay from moving to player if they collide
                    self.last_hit = time.time()
                
                # Print distance between the enemy
                # print(x_dist, y_dist)

        # Prevent enemey from hitting player if it has collided
        if time.time() - self.last_hit <= 2:
            # print("hit timeout", time.time() - self.last_hit)
            self.xPos += self.speedX
            self.yPos += self.speedY
        else:
            self.xPos += self.speedX * distX
            self.yPos += self.speedY * distY

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
    app.background = rgb(15, 14, 14)
    app.objective = Objective()
    app.player = Player(200, 200)
    app.enemies = []

    for i in range(2):
        app.enemies.append(Enemey())

main()

cmu_graphics.run()