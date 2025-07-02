import pyxel
import random

WIDTH = 360
HEIGHT = 240
TITLE = "T.O.W.E.R"

armes = {'fusil':(0,0,32,20),'pistolet':(1,40,32,15), 'sniper':(2,80,32,50), 'mitraillette':(3,120,32,8)}

map = [(0,0,WIDTH,5),(0,0,5,HEIGHT),(WIDTH-5,0,5,HEIGHT),(0,HEIGHT-5,WIDTH,5)]

class Player:
    def __init__(self):
        self.w = 24
        self.h = 32
        self.x = (WIDTH-self.w) /2
        self.y = (HEIGHT-self.h)/2
        self.vit = 3
        
        self.pv = 100
        
        self.anim = 0
        self.dir = 1
        
    def dessin(self):
        if pyxel.frame_count%12 < 6:
            self.anim = 0
        else:
            self.anim = self.w
        
        if pyxel.mouse_x < self.x + self.w/2:
            self.dir = -1
        else:
            self.dir = 1
        
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_Z):
            pyxel.blt(self.x,self.y,0,self.anim,0,self.dir*self.w,self.h,0)
        else:
            pyxel.blt(self.x,self.y,0,0,0,self.w*self.dir,self.h,0)
    
    def dessin_arme(self,arme):
        self.armx = self.x + self.w/2
        self.army = self.y + self.h/2
        self.arme = arme
        
        self.coo = (armes[self.arme][1],armes[self.arme][2])
        
        if abs(pyxel.mouse_x-self.armx) > abs(pyxel.mouse_y-self.army):
            if pyxel.mouse_x < self.armx:
                pyxel.blt(self.armx-14,self.army,0,self.coo[0],self.coo[1],-24,16,0)
            else:
                pyxel.blt(self.armx-10,self.army,0,self.coo[0],self.coo[1],24,16,0)
        else:
            if pyxel.mouse_y < self.army:
                if pyxel.mouse_x < self.armx:
                    pyxel.blt(self.armx-14,self.army-12,0,self.coo[0]+24,self.coo[1],16,-24,0)
                else:
                    pyxel.blt(self.armx-2,self.army-12,0,self.coo[0]+24,self.coo[1],-16,-24,0)
            else:
                if pyxel.mouse_x < self.armx:
                    pyxel.blt(self.armx-14,self.army,0,self.coo[0]+24,self.coo[1],-16,24,0)
                else:
                    pyxel.blt(self.armx-2,self.army,0,self.coo[0]+24,self.coo[1],16,24,0)
        
p = Player() 

class Bullet:
    def __init__(self, x=p.x, y=p.y, dx=0, dy=0, r = 2, vit = 8, dmg=10, c=9):
        pyxel.play(0,0)
        
        self.px = x + p.w/2
        self.py = y + p.h/2
        self.destx = dx
        self.desty = dy
        self.r = r
        self.vit = vit
        self.dmg = dmg
        self.coul = c
        
        
        self.dirx = (self.destx - self.px)
        self.diry = (self.desty - self.py)
        
        if abs(self.dirx) > abs(self.diry):
            self.diry = self.diry / abs(self.dirx)
            self.dirx = self.dirx / abs(self.dirx)
        else:
            self.dirx = self.dirx / abs(self.diry)
            self.diry = self.diry / abs(self.diry)
        
    def mvt(self):
        self.px += self.dirx * self.vit
        self.py += self.diry * self.vit
    
    def dessin(self):
        pyxel.circ(self.px,self.py,self.r,self.coul)
        

class Monstre:
    def __init__(self, x = 100, y = 100, type = 0):
        self.type = type
        self.x = x
        self.y = y
        
        self.cx = 1
        self.cy = 1
        
        if self.type == 0:  #normal
            self.w = 16
            self.h = 16
            self.vit = 1.5
            self.pv = 50
            self.coul = 12
        elif self.type == 1: #lourd
            self.w = 24
            self.h = 24
            self.vit = 1
            self.pv = 100
            self.coul = 4
        elif self.type == 2:  #tireur
            self.w =16
            self.h = 16
            self.vit = 0
            self.pv = 30
            self.coul = 2
        
    def depl(self):
        if self.x+1 < p.x:
            self.x += self.vit
        elif self.x-1 > p.x:
            self.x -= self.vit
        if self.y+1 < p.y:
            self.y += self.vit
        elif self.y-1 > p.y:
            self.y -= self.vit
            
    def damage(self):
        if self.type !=2:
            if p.x-self.w< self.x< p.x+p.w and p.y-self.h< self.y< p.y+p.h:
                p.pv -= 1
        
    def dessin_m(self):
        if self.x < p.x:
            self.cx = 1
        else:
            self.cx = -1
        if self.y < p.y+16:
            self.cy = 1
        else:
            self.cy = -1
        
        
        if self.type == 0:
            if self.cy == 1:
                if pyxel.frame_count%15 < 7:
                    pyxel.blt(self.x,self.y,0,0,88,self.w,self.h,0)
                else:
                    pyxel.blt(self.x,self.y,0,16,88,self.w,self.h,0)
            else:
                if pyxel.frame_count%15 < 7:
                    pyxel.blt(self.x,self.y,0,32,88,self.w,self.h,0)
                else:
                    pyxel.blt(self.x,self.y,0,48,88,self.w,self.h,0)
        
        elif self.type == 1:
            if abs(p.x-self.x) < abs(p.y-self.y):
                if self.cy == 1:
                    if pyxel.frame_count%20 < 10:
                        pyxel.blt(self.x,self.y,0,0,128,self.w,self.h,0)
                    else:
                        pyxel.blt(self.x,self.y,0,0,128,-self.w,self.h,0)
                else:
                    if pyxel.frame_count%20 < 10:
                        pyxel.blt(self.x,self.y,0,24,128,self.w,self.h,0)
                    else:
                        pyxel.blt(self.x,self.y,0,24,128,-self.w,self.h,0)
            else:
                if pyxel.frame_count%20 < 10:
                    pyxel.blt(self.x,self.y,0,48,104,self.w*self.cx,self.h,0)
                else:
                    pyxel.blt(self.x,self.y,0,48,128,self.w*self.cx,self.h,0)
        
        elif self.type == 2:
            if abs(p.x-self.x) < abs(p.y-self.y):
                pyxel.blt(self.x,self.y,0,0,72,self.w,self.h*self.cy,0)
            else:
                pyxel.blt(self.x,self.y,0,16,72,self.w*self.cx,self.h,0)


class Jeu:
    def __init__(self):
        pyxel.init(WIDTH,HEIGHT,title=TITLE, quit_key = pyxel.KEY_ESCAPE)
        
        self.enn = []
        self.bullets = []
        self.cam_x = 0
        self.cam_y = 0
        self.etage = 1
        self.gameover = False
        
        self.arm = 0
        self.maxarm = len(armes)-1
        self.armN = 'fusil'
        
        self.port_pos = (random.randint(23,WIDTH-33),random.randint(23,HEIGHT-33))
        self.medkit = None
        #self.medkit = (random.randint(7,WIDTH-33),random.randint(7,HEIGHT-33))
        self.alea_x = 0
        self.alea_y = 0
        
        self.chrono = 0
        self.anim = HEIGHT
        
        pyxel.mouse(False)
        pyxel.load('sources/res.pyxres')
        pyxel.run(self.update,self.draw)    
    
    
    def deplacement(self):
        if pyxel.btn(pyxel.KEY_Z) and p.y > 0:
            p.y -= p.vit
        if pyxel.btn(pyxel.KEY_S) and p.y+p.h < HEIGHT:
            p.y += p.vit
        if pyxel.btn(pyxel.KEY_D) and p.x+p.w < WIDTH:
            p.x += p.vit
        if pyxel.btn(pyxel.KEY_Q) and p.x > 0:
            p.x -= p.vit
    
    def tir(self):
        if pyxel.btnp(pyxel.KEY_E):
            self.arm += 1
            if self.arm > self.maxarm:
                self.arm = 0
        if pyxel.btnp(pyxel.KEY_A):
            self.arm -= 1
            if self.arm < 0:
                self.arm = self.maxarm
        
        if self.arm == 0:
            self.armN = 'fusil'
        elif self.arm == 1:
            self.armN = 'pistolet'
        elif self.arm == 2:
            self.armN = 'sniper'
        elif self.arm == 3:
            self.armN = 'mitraillette'
        
        if self.armN == 'fusil':
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count > self.chrono+6:
                self.bullets.append(Bullet(p.x,p.y,pyxel.mouse_x,pyxel.mouse_y,dmg=armes[self.armN][3]))
                self.chrono = pyxel.frame_count
        
        if self.armN == 'pistolet':
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count > self.chrono+1:
                self.bullets.append(Bullet(p.x,p.y,pyxel.mouse_x,pyxel.mouse_y, r=1, vit=7,dmg=armes[self.armN][3]))
                self.chrono = pyxel.frame_count
        
        if self.armN == 'sniper':
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count > self.chrono+30:
                self.bullets.append(Bullet(p.x,p.y,pyxel.mouse_x,pyxel.mouse_y, r=2, vit=14,dmg=armes[self.armN][3]))
                self.chrono = pyxel.frame_count
        
        if self.armN == 'mitraillette':
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count > self.chrono+2:
                self.bullets.append(Bullet(p.x,p.y,pyxel.mouse_x,pyxel.mouse_y, r=1, vit=7,dmg=armes[self.armN][3]))
                self.chrono = pyxel.frame_count
    
    def enn_mort(self):
        for enn in self.enn:
            for b in self.bullets:
                if b.coul ==9 and enn.x<b.px<enn.x+enn.w and enn.y<b.py<enn.y+enn.h:
                    enn.pv -= b.dmg
                    self.bullets.remove(b)
            
            if enn.pv <= 0:
                self.enn.remove(enn)
                
    def enn_tir(self):
        for enn in self.enn:
            if enn.type==2 and pyxel.frame_count%70==0:
                self.bullets.append(Bullet(enn.x,enn.y,p.x+p.w/2,p.y+p.h/2,vit=4,dmg=30,c=7))
                
    def player_dmg(self):
        for b in self.bullets:
            if b.coul!=9 and p.x<b.px<p.x+p.w and p.y<b.py<p.y+p.h:
                p.pv -= b.dmg
                self.bullets.remove(b)
                
    def heal(self):
        if self.medkit != None:
            if self.medkit[0]-p.w<p.x<self.medkit[0]+16 and self.medkit[1]-p.h<p.y<self.medkit[1]+16:
                self.medkit = None
                pyxel.play(2,2)
                
                if p.pv > 50:
                    p.pv = 100
                else:
                    p.pv += 50
    
    def dess_portail(self):
        if self.enn == []:
            pyxel.circ(self.port_pos[0],self.port_pos[1],16,6)
            
    def portail(self):
        if self.enn == []:
            if self.port_pos[0]-16<p.x<self.port_pos[0]+16 and self.port_pos[1]-16<p.y<self.port_pos[1]+16:
                pyxel.text(p.x-7,p.y-10,"Press SPACE",7)
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.nouvelle_salle()
                    self.etage += 1
                    
    def nouvelle_salle(self):
        pyxel.play(1,1)
        
        p.x = (WIDTH-p.w) /2
        p.y = (HEIGHT-p.h)/2
        self.anim = HEIGHT
        self.enn = []
        self.port_pos = (random.randint(23,WIDTH-33),random.randint(23,HEIGHT-33))
        self.medkit = (random.randint(7,WIDTH-33),random.randint(7,HEIGHT-33))
        
        for i in range(self.etage):
            self.alea_x = random.randint(8,WIDTH-24)
            self.alea_y = random.randint(8,HEIGHT-24)
            while p.x-64<self.alea_x<p.x+p.w+64 and p.y-64<self.alea_y<p.y+p.h+64:
                self.alea_x = random.randint(8,WIDTH-24)
                self.alea_y = random.randint(8,HEIGHT-24)
            self.enn.append(Monstre(self.alea_x,self.alea_y,random.randint(0,2)))

    
    def update(self):
        if self.gameover == False:
            pyxel.camera(self.cam_x, self.cam_y)
            self.deplacement()
            self.tir()
        
            for b in self.bullets:
                b.mvt()
                if b.px < self.cam_x-20 or self.cam_x+WIDTH+20 < b.px:
                    if b.py < self.cam_y-20 or self.cam_y+HEIGHT+20 < b.py:
                        self.bullets.remove(b)
            
            
            for enn in self.enn:
                enn.depl()
                enn.damage()
            self.enn_mort()
            self.enn_tir()
            
            self.player_dmg()
            
            self.heal()
        
        if p.pv <= 0:
            self.gameover = True
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.enn = []
                self.bullets = []
                self.etage = 1
                self.gameover = False
                
                self.arm = 0
                self.maxarm = len(armes)-1
                self.armN = 'fusil'
                
                self.port_pos = (random.randint(23,WIDTH-33),random.randint(23,HEIGHT-33))
                self.medkit = None
                #self.medkit = (random.randint(7,WIDTH-33),random.randint(7,HEIGHT-33))
                self.alea_x = 0
                self.alea_y = 0
                self.chrono = 0
                
                p.pv = 100
                p.x = (WIDTH-p.w) /2
                p.y = (HEIGHT-p.h)/2
                
        if self.anim > 0:
            self.anim -= 24
    
    
    def draw(self):
        pyxel.cls(0)
        if self.gameover == False:
            pyxel.bltm(0,0,0,0,0,WIDTH,HEIGHT,7)
            
            self.dess_portail()
        
            if self.medkit != None:
                pyxel.blt(self.medkit[0],self.medkit[1],0,16,56,16,16,0)
                
                
            if self.etage == 1:
                pyxel.blt(155,70,2,0,0,48,8,0)
                
                pyxel.text(140,100,"DEPLACEMENT : Z Q S D",7)
                pyxel.text(140,120,"CHANGE WEAPON : A E",7)
                pyxel.text(140,140,"FIRE : LEFT CLICK",7)
                
        
            for b in self.bullets:
                b.dessin()
        
            p.dessin()
            p.dessin_arme(self.armN)
        
            for enn in self.enn:
                enn.dessin_m()
            
            for m in map:
                pyxel.rect(m[0],m[1],m[2],m[3],7)
        
        
            pyxel.blt(pyxel.mouse_x-8,pyxel.mouse_y-8,0,0,56,16,16,0)
            self.portail()
            pyxel.text(8,8,"HP : "+str(p.pv),7)
            pyxel.text(8,16,"Floor : "+str(self.etage),7)
            
            pyxel.rect(0,0,WIDTH,self.anim,0)
            
        else:
            pyxel.text(150,100,"GAME OVER",7)
            pyxel.text(150,125,"Floor : "+str(self.etage),7)
            pyxel.text(130,150,"Press SPACE to replay",7)

Jeu()