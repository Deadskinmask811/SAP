import pygame
import sys
import random
from pygame.locals import *

#-----WINDOW DIMENSIONS-----
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

#-----COLORS------
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#-----HELPER FUNCTIONS-----
def terminate():
    pygame.quit()
    sys.exit

def drawText(text, color, x, y, surface):
    text = font.render(text, 1, color)
    textRect = text.get_rect()
    textRect.topleft = (x, y)
    surface.blit(text, textRect)
    
def waitForInput():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return
#-----END HELPER FUNCTIONS-----

#-----CLASSES-------
class Entity(object):
    def __init__(self, size, start_x, start_y, image, color, moveSpeed, hp):
        self.size = size # useful only when using an image surface instead of fill surface
        self.hp = hp
        self.alive = True
        self.start_x = start_x
        self.start_y = start_y
        self.image = image
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.rect.centerx, self.rect.centery = self.start_x, self.start_y
        
        self.move_speed = moveSpeed
        self.isShooting = False
        self.bulletList = []
        
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.shootTimer = 0
        self.shootFrequency = 50  

    def update(self, dt):
        self.shootTimer += dt
        # see if Entity is alive before proceeding       
        if not self.isAlive():
            print('poop')
            playing = False
            
        if self.moving_right and self.rect.right < WINDOWWIDTH:
            self.moveRight()
        if self.moving_left and self.rect.left > 0:
            self.moveLeft()
        if self.moving_up and self.rect.top > 0:
            self.moveUp()
        if self.moving_down and self.rect.bottom < WINDOWHEIGHT:
            self.moveDown()

        if self.isShooting and self.shootTimer >= self.shootFrequency:
            self.shoot(dt)
            self.shootTimer = 0 

    def isAlive(self):
        if self.hp <= 0:
            self.alive = False
        return self.alive

    def shoot(self, dt):
        if not self.isShooting:
            self.isShooting = True
        
        targetLocation = pygame.mouse.get_pos()
        self.newBullet = Projectile(self, targetLocation)    
            
    def startShoot(self):
        self.isShooting = True

    def stopShoot(self):
        self.isShooting = False

    def moveRight(self):
        if not self.moving_right:
            self.moving_right = True
            
        self.moving_left = False
        self.rect.move_ip(self.move_speed, 0)

    def moveLeft(self):
        if not self.moving_left:
            self.moving_left = True
        self.moving_right = False
        self.rect.move_ip(-1 * self.move_speed, 0)

    def moveUp(self):
        if not self.moving_up:
            self.moving_up = True
        self.moving_down = False
        self.rect.move_ip(0, -1 * self.move_speed)
    
    def moveDown(self):
        if not self.moving_down:
            self.moving_down = True
        self.moving_up = False
        self.rect.move_ip(0, self.move_speed)

    def stopRight(self):
        self.moving_right = False
    
    def stopLeft(self):
        self.moving_left = False

    def stopUp(self):
        self.moving_up = False

    def stopDown(self):
        self.moving_down = False
        
    def setHp(self, value): # universal function for changing hp, damage values get passed as negative and healing get passed as positive.
        self.hp += value
        
# these will most likely hold info about special shots/stats all base functionality in Entity parent
class Player(Entity):
    # this is here because python doesnt like empty classes
    def sayHi(self):
        print('sdlfkjsdf')
       
class Enemy(Entity):
    #this is here because python doesnt like empty classes
    def sayHi(self):
        print('sdlfksjd')

class Boss(Entity):
    def __init__(self, size, start_x, start_y, surface, color, moveSpeed, hp, name):
        super().__init__(size, start_x, start_y, surface, color, moveSpeed, hp)
        self.name = name
        print(self.name)
    
    def isAlive(self):
        if self.hp <= 0:
            self.alive = False
            print(self)
            hostileEntityList.remove(self)

        return self.alive

class Projectile(object):

    def __init__(self, Entity, target):
        self.entity = Entity 
        self.target = target
        self.size = 6
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = (self.entity.rect.centerx)
        self.rect.centery = (self.entity.rect.centery)

        self.movement = [None] * 2 # list to hold the movement vector for update()
        self.speed = 20

        self.start_x = self.entity.rect.centerx
        self.start_y = self.entity.rect.centery
        self.position = (self.rect.x, self.rect.y) 
        self.target_pos = self.target 
        self.target_pos_vector = pygame.math.Vector2(self.target_pos[0], self.target_pos[1])
        self.start_pos_vector = pygame.math.Vector2(self.start_x, self.start_y)
        self.angle = self.target_pos_vector - self.start_pos_vector
        self.direction = pygame.math.Vector2.normalize(self.angle)
        
        self.entity.bulletList.append(self)
        
    def doDamage(self, damageAmount, target):
        damageTaken = damageAmount * -1 # make damageAmount a negative number to pass to setHp on entity.
        target.setHp(damageTaken)

    def hasHitEntity(self, hostileEntityList):
        for h in hostileEntityList:
            if self.rect.colliderect(h) and isinstance(h, Boss): #check to see if boss is hit and reduce hp
                print('boss hit')
                self.doDamage(1, h) # do 1 damage to h 
                #hostileEntityList.remove(h)
                self.entity.bulletList.remove(self)

    def update(self, hostileEntityList):
        self.movement[0] = self.position[0] - self.rect.x
        self.movement[1] = self.position[1] - self.rect.y
        self.position += self.direction * self.speed  
       
        self.rect.move_ip(self.movement[0], self.movement[1])
        
        self.hasHitEntity(hostileEntityList)
        #print(self.entity.bulletList.count(self))
        if self.entity.bulletList.count(self) > 0:
            if self.rect.x < 0 or self.rect.x > WINDOWWIDTH or self.rect.y < 0 or self.rect.y > WINDOWHEIGHT:
                self.entity.bulletList.remove(self)



        
#-----END CLASSES-----

pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Shoot and Prosper')
font = pygame.font.SysFont(None, 32)

playing = True

#-----TITLE LOOP-----
while True:
    #-----MAIN TITLE SCREEN-----
    windowSurface.fill(BLACK)
    drawText('SHOOT AND PROSPER', WHITE, WINDOWWIDTH / 3, WINDOWHEIGHT / 3, windowSurface)
    pygame.display.update()
    waitForInput()

    #-----Entity SETUP------
    #--------Entity(size, x, y, surface, color, moveSpeed, hp)-----
    player = Player(5, WINDOWWIDTH / 2, WINDOWHEIGHT / 2, pygame.Surface([20, 20]), GREEN, 10, 10)
    #------Boss(size, x, y, surface, color, moveSpeed, hp, name)-----
    #boss = Boss(10, WINDOWWIDTH / 2, 100, pygame.Surface([50,50]), BLUE, 10, 15, "BIG BOSS") 
   
    hostileEntityList = []
    #hostileEntityList.append(boss)
    #print(hostileEntityList[0])
    while playing:

        dt = clock.tick(60) # delta time to keep track of event timing
        
        #-----EVENT TRACKING------
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == ord('d'):
                    player.moveRight()
                if event.key == ord('s'):
                    player.moveDown()
                if event.key == ord('a'):
                    player.moveLeft()
                if event.key == ord('w'):
                    player.moveUp()
                if event.key == K_SPACE:
                    player.startShoot()  

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.startShoot()               

            if event.type == KEYUP:
                if event.key == ord('d'):
                    player.stopRight()
                if event.key == ord('s'):
                    player.stopDown()
                if event.key == ord('a'):
                    player.stopLeft()
                if event.key == ord('w'):
                    player.stopUp()
                if event.key == K_SPACE:
                    player.stopShoot()
                   
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    player.stopShoot()
        #-----END EVENT TRACKING-----
        
        #spawn bosses just for testing
        if len(hostileEntityList) < 5:
            nb = Boss(10, random.randint(0, WINDOWWIDTH), random.randint(0, WINDOWHEIGHT), pygame.Surface([50,50]), BLUE, 10, 15, "BIGBOSS")
            hostileEntityList.append(nb)

        #-----UPDATE INFORMATION-----
        player.update(dt)
        if len(hostileEntityList) > 0:
            for e in hostileEntityList:
                e.update(dt)
        # update all info for bullets belonging to player
        for b in player.bulletList:
            b.update(hostileEntityList)

        #-----DRAW INFO TO SCREEN-----
        windowSurface.fill(BLACK)    
        windowSurface.blit(player.image, player.rect)
        for e in hostileEntityList:
            windowSurface.blit(e.image, e.rect)
        for b in player.bulletList:
            windowSurface.blit(b.image, b.rect)

        pygame.display.update()
        clock.tick(60)
       
windowSurface.fill(BLACK)
pygame.display.update()
