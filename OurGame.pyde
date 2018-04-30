import os

path=os.getcwd()

class Game:
    def __init__(self):
        self.w=500
        self.h=700
        self.state='start'
        
    def create(self):
        self.enemies=[]
        resources = open(path+'\\resources\\state game'+'.csv','r')
        for item in resources:
            item = item.strip().split(",")
            if item[0] == 'Hero':
                self.hero = Hero(int(item[1]),int(item[2]),int(item[3]),item[4],int(item[5]))
            elif item[0] == 'Enemy':
                self.enemies.append(Enemy(int(item[1]),int(item[2]),int(item[3]),item[4],int(item[5])))
        resources.close()
        
    def display(self):
        for e in self.enemies:
            e.display()
        self.hero.display()
        
        
class Npc:
    def __init__(self,x,y,r,imgName,g):
        self.x=x
        self.y=y
        self.r=r
        self.w=self.r*2
        self.h=self.r*2
        self.xv=0
        self.yv=0
        self.g=g
        self.img=loadImage(imgName)
    
    def display(self):
        #how to make it different for hero and enemies
        image(self.img,self.x-self.r,game.w+self.y+2*self.r,self.w,self.h,)
        self.update()
    
        
#    def gravity(self):
# kill meeeee
            
        
class Hero(Npc):
    def __init__(self,x,y,r,imgName,g):
        Npc.__init__(self,x,y,r,imgName,g)
        self.keyHandler={LEFT:False,RIGHT:False,UP:False}
        
    def update(self):
        if self.keyHandler[LEFT]:
            self.xv=-3
        elif self.keyHandler[RIGHT]:
            self.xv=3
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ WTF IS DIR @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ = direction
        elif self.keyHandler[UP] and self.yv >= 0:
            self.yv=-3
            
        else:
            self.xv=0
            self.xy=0
            
        self.x+=self.xv    
        self.y+=self.yv        
        
class Enemy(Npc):
    def __init__(self,x,y,r,imgName,g):
        Npc.__init__(self,x,y,r,imgName,g)
        self.vx = 1
        
    def update(self):
        "not done yet"
        
        
    
game=Game()

def setup():
    background(0)
    size(game.w,game.h)
    game.create()
    
def draw():
    textSize(40)
    if game.state=='start':
        if game.w//2.8<=mouseX<=game.w//2.8+130 and game.h//2-40<=mouseY<=game.h//2:
            fill(255,255,100)
        else:    
            fill(255,255,0)
        text('START',game.w//2.8,game.h//2)
    if game.state=='game':
        background(0)
        game.display()

def mouseClicked():
    if game.state=='start' \
    and game.w//2.8<=mouseX<=game.w//2.8+130 and game.h//2-40<=mouseY<=game.h//2:
        game.state='game'
        
def keyPressed():
    if game.state=='start' and keyCode==10:
       game.state='game'
       
    if game.state=='game':
        game.hero.keyHandler[keyCode]=True   
        
def keyReleased():
    if game.state=='game':
        game.hero.keyHandler[keyCode]=False
