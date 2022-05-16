# Fill me in!
from cmu_graphics import *


app.colors = ['red', 'yellow', 'green', 'saddleBrown', 'white']
app.stepsPerSecond = 100

#sky
app.background = "skyBlue"
#Grass
sun = Rect(0,350,400,350,fill="paleGreen")

#Sun
sun = Group(
    Star(390, 10, 35, 25, roundness=50, fill="yellow"),
    Circle(390,10, 25, fill="yellow")
    )
    
trees = Group()
clouds = Group()

headCenterX = 100
headCenterY = 250
hipX, hipY = getPointInDir(headCenterX ,headCenterY, 190, 80)
head = Oval(headCenterX, headCenterY, 30, 45, fill="black")
body = Line(headCenterX, headCenterY, hipX, hipY)
shoulderX, shoulderY = getPointInDir(headCenterX, headCenterY, 190, 40)



app.armAngleLeft = 250
app.armAngleRight = 110
#armLeft = Line(headCenterX, headCenterY, shoulderX, shoulderY)
xRightArm, yRightArm = getPointInDir(shoulderX, shoulderY, app.armAngleRight, 30)
xLeftArm, yLeftArm = getPointInDir(shoulderX, shoulderY, app.armAngleLeft, 30)
xRightLeg, yRightLeg = getPointInDir(hipX, hipY,app.armAngleRight,40)
xLeftLeg, yLeftLeg = getPointInDir(hipX,hipY,app.armAngleLeft,40)

armRight = Line(shoulderX, shoulderY, xRightArm, yRightArm, fill="black")
armLeft = Line(shoulderX, shoulderY, xLeftArm, yLeftArm, fill="black")
legRight = Line(hipX, hipY,xRightLeg,yRightLeg)
legLeft = Line(hipX,hipY,xLeftLeg,yLeftLeg)


completeBody = Group(head, body, armRight, armLeft,legRight,legLeft)

app.wayRight = 1
app.wayLeft = -1

def drawManyCircles(number):
    for i in range(1,number):
        
        pass
    pass


def drawTree():
    tree = Rect(180,260,40,100,fill="saddleBrown")
    Star(200,215,80,50,fill="green",roundness=95)
    Star(200,215,50,30,fill=gradient("paleGreen","green"),roundness=95)

def drawCloud(num = 1):
    for i in range(num):
        randX = randrange(100, 350)
        randY = randrange(50, 150)
        cloud = Group(
            Circle(randX, randY, 20, fill = "white"),
            Circle(randX - 30, randY, 20, fill = "white"),
            Circle(randX + 30, randY, 20, fill = "white"),
    
            Circle(randX - 15, randY - 20, 20, fill = "white"),
            Circle(randX + 15, randY - 20, 20, fill = "white"),
            
            Circle(randX - 15, randY + 20, 20, fill = "white"),
            Circle(randX + 15, randY + 20, 20, fill = "white"), 
        )
    clouds.add(cloud)
    
drawCloud()
drawTree()

def onStep():
    for cloud in clouds:
        if cloud.centerX <= 0:
            cloud.centerX = 400
        else:
            cloud.centerX -= 1
        
    #for angle1 in range(110, 250, 1):
    
    if app.armAngleRight > 250:
        app.wayRight = -app.wayRight
        app.wayLeft = -app.wayLeft
    
    if app.armAngleRight < 110:
        app.wayRight = -app.wayRight
        app.wayLeft = -app.wayLeft
        
    handxRight, handyRight = getPointInDir(shoulderX, shoulderY, app.armAngleRight, 30)
    handxLeft, handyLeft = getPointInDir(shoulderX, shoulderY, app.armAngleLeft, 30)
    footxRight, footyRight = getPointInDir(hipX,hipY,app.armAngleRight,40)
    footxLeft,footyLeft = getPointInDir(hipX,hipY,app.armAngleLeft,40)
    armRight.x2 = handxRight
    armRight.y2 = handyRight
    legRight.x2 = footxRight
    legRight.y2 = footyRight
    
    armLeft.x2 = handxLeft
    armLeft.y2 = handyLeft
    legLeft.x2 = footxLeft
    legLeft.y2 = footyLeft
    
    app.armAngleRight += 2 * app.wayRight
    app.armAngleLeft += 2 * app.wayLeft

    #for part in completeBody:
        #part.centerX += 1

cmu_graphics.run()
