"""
This thing simulates living in space. People cannot if the don't have protection while cyborgs always can surive.
"""


from cmu_graphics import *

# Fill me in!

app.background = 'black'
app.objects = []
app.feelings = ['happnies', 'sadness', 'meh']
app.stepsPerSecond = 5

app.stars = Group()

class Person(object):
    def __init__(self, x, y):
        self.dx = 0
        self.dy = 1
        self.type = "person"
        self.draw(x, y)
        self.change_emotion()
        self.set_name()
        self.protection(x, y)
            
    def protection(self, x, y):
        r = randrange(0,100)
        if r < 20:
            self.has_protection = True
            space_helmet = Rect(x - 25, y - 25, 50, 50, border= "red", fill=None)
            self.drawing.add(space_helmet)
        else:
            self.has_protection = False
        
            
    def draw(self, x, y):
        
        self.drawing = Group(
            Line(x, y, x, y+70, fill="white"),
            Line(x, y + 70, x-10, y+70+25, fill="white"), # Left Leg
            Line(x, y + 70, x+10, y+70+25, fill="white"), # Right Leg
            
            Line(x, y+20, x-15, y+45, fill="white"), # Left Arm
            Line(x, y+20, x+15, y+45, fill="white"), # Right arm        
    
            Circle(x, y, 20, border='white', fill='black'),
            

            
            )
        #self.drawing.center = self.drawing.centerY + 70
    
    def change_emotion(self):
        self.emotion = app.feelings[randrange(len(app.feelings))]
    
    def set_name(self):
        self.name = f'Player{randrange(100, 999)}'
    
    def move(self):
        #gravity = self.gravitational_pull(1)
        #self.Dy += gravity
        self.drawing.centerY += 9.82
    
    def reset(self):
        self.drawing.centerY = 0
        
    def death(self):
        app.objects.remove(self)
        print(f"{self.name} could not surrvive outer space")
        
    def check_colission(self):
        for o in app.objects:
            if self.drawing.hitsShape(o.drawing):
                o.death()
                self.death()
    
class Cyborg(Person):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "cyborg"
        
    def draw(self, x, y):
        self.head_size = randrange(20,30)
        scaler = self.head_size // 4
        self.drawing = Group(
            Line(x, y, x, y+70 - scaler, fill="white"),
            Rect(x - (self.head_size//2), y, self.head_size, self.head_size, border='white', fill='black'),
            
            Line(x, y + 70 - scaler, x-10, y+70+25, fill="white"), # Left Leg
            Line(x, y + 70 - scaler, x+10, y+70+25, fill="white"), # Right Leg
            
            Line(x, y+self.head_size, x-15, y+40, fill="white"), # Left Arm
            Line(x, y+self.head_size, x+15, y+40, fill="white"), # Right arm   
            
            )
    
def onStep():
    for obj in app.objects:
        #obj.check_colission()
        
        if obj.drawing.centerY < 500:
            #print(obj.drawing.centerY)
            obj.move()
        else:
            if obj.type == "person" and not obj.has_protection:
                obj.death()    
                continue
            else:
                obj.reset()
                if obj.type == "person" and obj.has_protection:
                    print(f"{obj.name} is a {obj.type} and they can survive in space because they have protection!")
                else:
                    print(f"{obj.name} is a {obj.type} and they can always survive in space!")
            

def onMousePress(mouseX, mouseY):
    random = randrange(0, 100)
    
    if random > 50:
        p = Person(mouseX, mouseY)
    else:
        p = Cyborg(mouseX, mouseY)
        
    print(f'Yo im {p.name}, I feel {p.emotion}')
    p.change_emotion()
    print(f'{p.name} feels {p.emotion}')
    app.objects.append(p)
        
        
cmu_graphics.run()
    