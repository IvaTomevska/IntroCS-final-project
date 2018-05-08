add_library('minim')

import os

path=os.getcwd()
minim=Minim(this);

class Game:
    def __init__(self):
        self.w=1000
        self.h=700
        self.g=0
        self.state='start'
        self.platforms=[]
        self.scoretime = 10
        self.cnt = 0
        
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
            elif item[0]=='End':
                self.stage_y_end = int(item[1])
        resources.close()
        
        self.soundtrack=minim.loadFile (path+"\\resources\\Soundtrack.mp3",2048)
        self.soundtrack.play() 
        self.bgmusic=minim.loadFile (path+"\\resources\\Background.mp3",2048)
    
        
    def display(self):
        for p in self.platforms:
            p.display()
            
        for e in self.enemies:
            e.display()
        self.hero.display()
        
            
        if self.hero.y>500:#fix here for start of coutdown of time
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
            self.yv-=0.2
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
            self.yv=+10
            self.jump+=1
            
        else:
            self.xy=0
            
        self.x+=self.xv    
        self.y+=self.yv  
        
        # collision
        ctr=0
        for e in game.enemies:
            if self.distance(e) < self.r+e.r:
            #-self.r so that enemy won't be killed if hit in the lower half
                # if e.img=="vader.png":
                #     if self.y-self.r > e.y and self.yv < 0:
                #         while ctr!=3:
                #             self.killsound=minim.loadFile (path+"\\resources\\Lightsaber.mp3",2048)
                #             self.killsound.play()
                #             game.enemies.remove(e)
                #             self.yv = 5
                #             game.enemies.image(e)
                #             crt+=1
                #         del e
                #     else:
                #         game.__init__()
                #         game.create()
                        
                if self.y-self.r > e.y and self.yv < 0:
                    self.killsound=minim.loadFile (path+"\\resources\\Lightsaber.mp3",2048)
                    self.killsound.play()
                    game.enemies.remove(e)
                    del e
                    self.yv = 5
                    game.scoretime += 10

                else:
                    game.__init__()
                    game.create()
                    
        "moving in the middle"            
        if self.y >= game.h//2 and self.y < game.stage_y_end-game.h//2:
            game.h += self.yv

                    
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
        for p in game.platforms:
            if self.y==p.y+1:
                if self.x+self.r >= p.x+p.w:
                    self.xv=-2
                elif self.x-self.r <= p.x: 
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
        game.soundtrack.pause()
        game.bgmusic.play()
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
