import os

path=os.getcwd()

class Game:
    def __init__(self):
        self.w=1000
        self.h=700
        self.g=0
        self.state='start'
        self.platforms=[]
        self.scoretime = 10
        self.cnt = 0
        #self.time = 5
        
    def create(self):
        self.enemies=[]
        resources = open(path+'\\resources\\state game'+'.csv','r')
        for item in resources:
            item = item.strip().split(",")
            if item[0] == 'Hero':
                #x,y,r,path,g
                self.hero = Hero(int(item[1]),int(item[2]),int(item[3]),item[4],int(item[5]))
            elif item[0] == 'Enemy':
                self.enemies.append(Enemy(int(item[1]),int(item[2]),int(item[3]),item[4],int(item[5])))
            elif item[0] == 'Platform':
                #x,y,w,h,path
                self.platforms.append(Platform(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5]))
        resources.close()
        
        #self.platforms.append(Platform(200,250,300,100,'resources\\platform.png')) 
        
    def display(self):
        for e in self.enemies:
            e.display()
        self.hero.display()
        
        for p in self.platforms:
            p.display()
            
        if self.hero.y>2:#fix here for start of coutdown of time
            self.cnt  = (self.cnt + 1)%60
            if self.cnt == 0:
                self.scoretime-=1
            
        fill(255)
        text(str(self.scoretime), 20, 45)
        #text(str(self.time), 20, 80)
        if self.scoretime<=0:
                game.__init__()
                game.create()
        
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
        self.jump=0
    
    def display(self):
        #how to make it different for hero and enemies
        image(self.img,self.x-self.r,game.h-self.y-self.h,self.w,self.h,)
        self.update()
    
        
    def gravity(self):
        if self.y > self.g:
            self.yv-=0.1
            if self.y + self.yv < self.g:
                self.yv = self.g -self.y

        else:
            self.yv=0
            self.jump=0
            
        for p in game.platforms:
            if self.x+self.r >= p.x and self.x-self.r <= p.x+p.w and self.y >= p.y : 
                self.g = p.y
                break
            else:
                self.g=game.g
            
        
class Hero(Npc):
    def __init__(self,x,y,r,imgName,g):
        Npc.__init__(self,x,y,r,imgName,g)
        self.keyHandler={LEFT:False,RIGHT:False,UP:False,65:False,68:False,87:False,32:False}
        
    def update(self):
        self.gravity()
        
        if self.keyHandler[LEFT] or self.keyHandler[65]:
            self.xv=-3
        elif self.keyHandler[RIGHT] or self.keyHandler[68]:
            self.xv=3
        else:
            self.xv=0
        if (self.keyHandler[UP] or self.keyHandler[87] or self.keyHandler[32]) and self.yv >= 0 and self.jump<1:
            self.yv=+7.5
            self.jump+=1
            
        else:
            self.xy=0
            
        self.x+=self.xv    
        self.y+=self.yv  
        
        # collision
        for e in game.enemies:
            if self.distance(e) < self.r+e.r:
                #-self.r so that enemy won't be killed if hit in the lower half
                if self.y-self.r > e.y and self.yv < 0:
                    game.enemies.remove(e)
                    del e
                    self.vy = 4
                    game.scoretime += 10
                else:
                    game.__init__()
                    game.create()

                    
    def distance(self,enemy):
        return ((self.x-enemy.x)**2+(self.y-enemy.y)**2)**0.5        
        
class Platform:
    def __init__(self,x,y,w,h,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img=loadImage(path+'\\'+img)
    
    def display(self):
        image(self.img,self.x,game.h-self.y)
        
class Enemy(Npc):
    def __init__(self,x,y,r,imgName,g):
        Npc.__init__(self,x,y,r,imgName,g)
        self.xv = 2        
        
    def update(self):
        if self.x+self.r >= game.w: 
            self.xv=-2
        elif self.x-self.r <= 0: 
            self.xv=2
        
        self.x+=self.xv
        self.y+=self.yv
        
    
game=Game()

def setup():
    background(0)
    size(game.w,game.h)
    game.create()
    
def draw():
    textSize(40)
    if game.state=='start':
        background(0)
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
