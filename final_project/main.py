from ast import Del
from this import d
from cmu_graphics import *
import time
# Fill me in!

class Game(object):
    def __init__(self):
        self.game_over = False
        self.player_score = 0
        self.score_label = Label(f"Score: {self.player_score}", 40, 25, fill="white", size=20)

        self.stars = Group()

        for t in range(150):
            r = randrange(1, 3)
            x = randrange(0 + r, 400-r)
            y = randrange(0 + r, 400-r)
            opac = randrange(0, 100)

            c = Circle(x, y, r, opacity=opac,fill="white")
            self.stars.add(c)
    
    def animate_stars(self):
        for star in self.stars:
            current_opac = star.opacity

            if current_opac <= 25:
                print("0 opacity")
                star.opacity = randrange(current_opac, current_opac + 30)
                continue
            # change_val = 2

            change_val = randrange(-1, 1) 

            # print(current_opac, current_opac - change_val, current_opac + change_val)

            if current_opac + change_val >= 100:
                change_val = 0
            elif current_opac + change_val <= 0:
                change_val = abs(change_val)

            star.opacity = current_opac + change_val

    def show_game_over(self):
        self.game_over_screen = Group(
            Rect(0, 0, 400, 400),
            Label("Game Over", 200, 200, size=50, fill="red"),
            Label(f"You got {self.player_score} points", 200, 235, size=25, fill="red"),
            Label("Press R to restart", 200, 260, size=15, fill="RED")
        )
        self.game_over_screen.toFront()
        


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

        self.update()


    def update(self):
        # Update screen
        self.drawing.centerX = self.xPos
        self.drawing.centerY = self.yPos
        
        if self.angle >= 360:
            self.angle = 0

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
        self.r = 12.5
        self.xPos = randrange(0 + rounded(self.r), 400 - rounded(self.r))
        self.yPos = randrange(0 + rounded(self.r), 400 - rounded(self.r))
        

        drawing = Group(
            Star(self.xPos, self.yPos, self.r, 5, fill="gold")
        )
        
        super().__init__(drawing=drawing)

        self.update()
    
    def newPos(self):
        self.xPos = randrange(0 + rounded(self.r), 400 - rounded(self.r))
        self.yPos = randrange(0 + rounded(self.r), 400 - rounded(self.r))

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

        # make sure not to collide with other enemies
        for enemy in enemies:
            # Dont check for itself
            if enemy.drawing != self.drawing:
                if enemy.drawing.hitsShape(self.drawing):
                    self.speedX *= -1
                    self.speedY *= -1

                    self.xPos += self.speedX + 1
                    self.yPos += self.speedY + 1

                    # Add delay from moving to player if they collide
                    self.last_hit = time.time()

                    # Update display
                    self.update()

        # if the enemies has hit eachother it shouldnt follow the player for 2 seconds
        if time.time() - self.last_hit <= 2:
            tempX = self.xPos + self.speedX
            tempY = self.yPos + self.speedY
        else:
            tempX = self.xPos + self.speedX * distX
            tempY = self.yPos + self.speedY * distY


        if tempX >= 400 - self.w:
            self.speedX *= -1
            # self.angle += 45
        elif tempX <= 0 + self.w:
            self.speedX *= -1
            # self.angle += 45
            
        if tempY  >= 400 - self.h:
            self.speedY *= -1
            # self.angle += 45
        elif tempY <= 0 + self.h:
            self.speedY *= -1
            # self.angle += 45

        # Prevent enemey from hitting player if it has collided
        self.xPos = tempX
        self.yPos = tempY

        self.update()


def onKeyHold(keys):
    if app.game.game_over and ("R" in keys or "r" in keys):
        print("restart")

        # Clears global canvas
        app.group.clear()
        
        # Redefine all variables
        main()

    if "W" in keys or "w" in keys or "up" in keys:
        app.player.dir[1] = -1

    if "D" in keys or "d" in keys or "right" in keys:
        app.player.dir[0] = 1

    if "S" in keys or "s" in keys or "down" in keys:
        app.player.dir[1] = 1

    if "A" in keys or "a" in keys or "left" in keys:
        app.player.dir[0] = -1

def onKeyPress(key):
    if app.game.game_over and ("R" == key or "r" == key):
        print("restart")

        # Clears global canvas
        app.group.clear()
        
        # Redefine all variables
        main()

app.numOfSteps = 0
def onStep():
    # Game loop
    if app.game.game_over:
        return

    app.numOfSteps += 1

    # app.player.drawing.toFront()
    if app.objective.drawing.hitsShape(app.player.drawing):
        app.score += 1
        app.game.player_score += 1

        app.objective.newPos()

        # Every 10 points add a enemey
        if app.score % 10 == 0:
            app.enemies.append(Enemey())
       
        app.game.score_label.value = f"Score: {app.game.player_score}"

    
    for enemy in app.enemies:
        if enemy.drawing.hitsShape(app.player.drawing):
            app.game.game_over = True
            print("Game Over")
            app.game.show_game_over()
            return

        enemy.move(app.player, app.enemies)

    app.player.move()
    if app.numOfSteps % 5 == 0:
        app.game.animate_stars()
        app.numOfSteps = 0


# Initial start create player instance and enemies
def main():
    # Define game stuff
    app.game = Game()
    app.background = rgb(15, 14, 14)
    app.objective = Objective()
    app.player = Player(200, 200)
    app.enemies = []
    app.score = 0
    app.GameOver = False

    for i in range(2):
        app.enemies.append(Enemey())

main()

cmu_graphics.run()