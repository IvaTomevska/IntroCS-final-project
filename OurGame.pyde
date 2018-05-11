add_library('minim')

import os, operator

path=os.getcwd()
minim=Minim(this);

class Game:
    def __init__(self):
        self.w=1000
        self.h=700
        self.hh=700
        self.g=0
        self.state='start'
        self.platforms=[]
        self.scoretime = 5
        self.cnt = 0
        self.vader = 3 # how many time before Vader is killed
        self.vaderPush = False
        self.cntVader = 0
        self.win="You won!\nbut you've also killed your father :("
        self.loss="You lost.\nThe Empire really stroke back."
        self.startText="In a galaxy far, far away\nin alternative Star Wars\nuniverse Luke found himself\nstuck on some clouds.\nThe only way for him to\nescape is to beat Darth Vader\nwho's standing above.\nHint: You better start killing\nthose stormtroopers."
        self.name=''
        self.hscore=[]
         
    def create(self):
        self.enemies=[]
        resources = open(path+'\\resources\\state game'+'.csv','r')
        for item in resources:
            item = item.strip().split(",")
            if item[0] == 'Hero':
                #x,y,r,path,g
                self.hero = Hero(int(item[1]),int(item[2]),int(item[3]),item[4],int(item[5]))
            elif item[0] == 'Enemy':
                self.enemies.append(Enemy(int(item[1]),int(item[2]),int(item[3]),item[4],int(item[5]),item[6]))
            elif item[0] == 'Platform':
                #x,y,w,h,path
                self.platforms.append(Platform(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5]))
            elif item[0]=='End':
                self.stage_y_end = int(item[1])
        resources.close()
        
        self.soundtrack=minim.loadFile (path+"\\resources\\Soundtrack.mp3",2048)
        self.bgmusic=minim.loadFile (path+"\\resources\\Background.mp3",2048)
        self.soundtrack.play() 
    
        
    def display(self):
        for p in self.platforms:
            p.display()
            
        for e in self.enemies:
            e.display()
        
        if self.vaderPush == True: #poor flying hero
            self.hero.x -= 24
            self.cntVader += 1
            if self.cntVader == 20:
                self.vaderPush = False
                self.cntVader = 0
                
        
        self.hero.display()
        
            
        if self.hero.y>500:#fix here for start of coutdown of time
            self.cnt  = (self.cnt + 1)%60
            if self.cnt == 0:
                self.scoretime-=1
            
        fill(255)
        text(str(self.scoretime), 20, 45)
        #text(str(self.time), 20, 80)
        if self.scoretime<=0:
                game.state='loss'
                game.h=game.hh
                
    def highscore(self):
            name=open(path+'\\resources\\highscore.csv','a')
            name.write(game.name+','+str(game.scoretime)+'\n')
            name.close()
            name=open(path+'\\resources\\highscore.csv','r')
            for i in name:
                temp=[i.strip().split(',')]
                temp[0][1]=int(temp[0][1]) #lambda didn't work?
                self.hscore+=temp
            self.hscore.sort(key=operator.itemgetter(1), reverse=True)
            if len(self.hscore) >= 10:
                self.bestTen=10
            else:
                self.bestTen=len(self.hscore)
        
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
        if game.state=='game':
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
            
            #going out of the screen
            if self.x < 0 or self.x > game.w:
                game.state='loss'                
            
            # collision
            for e in game.enemies:
                if self.distance(e) < self.r+e.r:
                #self.r so that enemy won't be killed if hit in the lower half                        
                    if self.y-self.r > e.y and self.yv < 0:
                        self.killsound=minim.loadFile (path+"\\resources\\Lightsaber.mp3",2048)
                        self.killsound.play()
                        if e.type=="v" and game.vader != 1:
                            game.vader-=1
                            self.y += self.r
                            self.yv = 4
                            game.vaderPush = True
                        elif e.type=='v' and game.vader==1:
                            game.scoretime += 100
                            game.state='win'
                        else:
                            game.enemies.remove(e)
                            del e
                            self.yv = 5
                            game.scoretime += 7
        
                    else:
                        game.state='loss'
                        
            #"moving in the middle"            
            if self.y >= game.h//2 and self.y < game.stage_y_end-game.h//2:
                game.h += self.yv
            if self.y+self.yv < game.hh//2:
                game.h = game.hh
                    
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
    def __init__(self,x,y,r,imgName,g,type):
        Npc.__init__(self,x,y,r,imgName,g)
        self.xv = 2        
        self.type=type
    def update(self):
        if game.state=='game':
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
    textSize(20)
    fill(255,255,0)
    background(0)
    if game.state=='start':
        text(game.startText,500,250)
        if game.w//5<=mouseX<=game.w//5+130 and game.h//2-40<=mouseY<=game.h//2:
            fill(255,255,100)
        textSize(40)
        text('START',game.w//5,game.h//2)
    elif game.state=='game':
        game.soundtrack.pause() 
        game.bgmusic.play()
        game.display()
    elif game.state=='win' or game.state=='loss':
        game.h=game.hh
        if game.state=='win':
            text(game.win,game.w//2,game.h//4)
        elif game.state=='loss':
            text(game.loss,game.w//2,game.h//4)
        text ('Enter your name (max 20 characters):',game.w//2,game.h//2)
        text(game.name,game.w//2,game.h//1.5)
        textSize(40)
        if game.w//5<=mouseX<=game.w//5+260 and game.h//2-40<=mouseY<=game.h//2:
            fill(255,255,100)
        text('PLAY AGAIN',game.w//5,game.h//2)
    elif game.state=='highscore':
        for i in range(game.bestTen):
            text(game.hscore[i][0],game.w//2,300+i*30)   
        for i in range(game.bestTen):
            text(game.hscore[i][1],game.w-100,300+i*30)
        textSize(40)
        if game.w//5<=mouseX<=game.w//5+260 and game.h//2-40<=mouseY<=game.h//2:
            fill(255,255,100)
        text('PLAY AGAIN',game.w//5,game.h//2)
        text('Best 10:',game.w//2,200)

def mouseClicked():
    if game.state=='start' \
    and game.w//5<=mouseX<=game.w//5+130 and game.h//2-40<=mouseY<=game.h//2:
        game.state='game'
    elif game.state=='win' or game.state=='loss' or game.state=='highscore'\
    and game.w//5<=mouseX<=game.w//5+260 and game.h//2-40<=mouseY<=game.h//2:
        game.state='start'
        game.bgmusic.pause()
        game.__init__()
        game.create()
        
def keyPressed():
    
    print(game.hero.y, game.h, game.hero.yv)
    
    if game.state=='start' and keyCode==10:
       game.state='game'
       
    elif game.state=='game':
        game.hero.keyHandler[keyCode]=True  
    
    elif game.state=='win' or game.state=='loss':
        if type(key) != int and keyCode != 10  and len(game.name) < 20:
            game.name += key
        if keyCode==8:
            game.name=game.name[:-2]
        if keyCode == 10 and len(game.name)>1:
            game.highscore()
            game.state='highscore'
            
    elif game.state=='highscore' and keyCode==10:    
        game.state='start'
        game.bgmusic.pause()
        game.__init__()
        game.create()
        
        
def keyReleased():
    if game.state=='game':
        game.hero.keyHandler[keyCode]=False
