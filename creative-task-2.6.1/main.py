# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# Fill me in!
from cmu_graphics import *
app.stepsPerSecond = 1
app.squareSize = 400 // 5

print(app.squareSize)

app.statusColors = [rgb(0,0,0), rgb(255,255,255)]
app.grid = []

    
def countNeighbours(row, col):
    #s = sum([1 for row in app.grid for cell in row if cell.fill == app.statusColors[1]])
    
    sum = app.grid[row][col].status
    sum += app.grid[row][col - 1].status
    sum += app.grid[row][col + 1].status
    sum += app.grid[row - 1][col].status
    sum += app.grid[row + 1][col].status
    sum += app.grid[row - 1][col -1].status
    sum += app.grid[row + 1][col + 1].status
    sum += app.grid[row + 1][col -1].status
    sum += app.grid[row - 1][col + 1].status
    
    return sum
    #print(s)
    
    # List = 3d-array    
    # Y N Y
    # N Y N
    # Y N N
    # return sum(^) = 3
    
    #print(s)
    


# Drawing out a grid of squares 
def drawGrid():
    
    for row in range(0,400, app.squareSize):
        rad = []
        for col in range(0, 400, app.squareSize):
            status = randrange(10, 200) % 2
            cell = Rect(row, col, row + app.squareSize, col+app.squareSize, fill=app.statusColors[status])
            cell.status = status
            rad.append(cell)
        
        app.grid.append(rad)    

drawGrid()

def onStep():
    for row in range(1, len(app.grid) - 1):
        for col in range(1, len(app.grid) - 1):
            sum = countNeighbours(row, col)
            print(sum)
            
            if 3 < sum > 2:
                app.grid[row][col].status = 1
            elif app.grid[row][col].status == 0 and sum == 3:
                app.grid[row][col].status = 1
            else:
                app.grid[row][col].status = 0
                # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
            #Rect(row, col, row + app.squareSize, col+app.squareSize, fill=app.statusColors[app.grid[row][col].status])
            
    

# Not updated rexts :(
cmu_graphics.run()
        