import pygame
import sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 700

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
    def __init__(self, start_x, start_y, image, color, moveSpeed):
        self.size = size
        self.start_x = start_x
        self.start_y = start_y
        self.image = image
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.rect.topleft = (self.start_x, self.start_y)
        
        self.move_speed = moveSpeed
        self.isShooting = False
        self.bulletList = []
        


class Player(Entity):
    def __init__(self):
        self.size = 25
        self.start_x = (WINDOWWIDTH / 2) - self.size
        self.start_y = WINDOWHEIGHT - 100
        self.image = pygame.Surface([self.size, self.size])
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.topleft = (self.start_x, self.start_y)

        self.moving_right = None 
        self.moving_left = None
        self.moving_up = None
        self.moving_down = None
        
        self.move_speed = 6 

        self.isShooting = False
        self.bulletList = []

    def update(self):
        if self.moving_right and self.rect.right < WINDOWWIDTH:
            self.moveRight()
        if self.moving_left and self.rect.left > 0:
            self.moveLeft()
        if self.moving_up and self.rect.top > 0:
            self.moveUp()
        if self.moving_down and self.rect.bottom < WINDOWHEIGHT:
            self.moveDown()

        if self.isShooting:
            self.shoot()

    def shoot(self):
        if not self.isShooting:
            self.isShooting = True
        self.newBullet = Projectile(self)    

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
        
        
class Projectile(object):

    def __init__(self, Player):
        self.player = Player
        self.size = 10 
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.player.rect.centerx, self.player.rect.centery)

        self.movement = [None] * 2 # list to hold the movement vector for update()
        self.speed = 5

        self.start_x = self.player.rect.centerx
        self.start_y = self.player.rect.centery
        self.position = (self.rect.x, self.rect.y) 
        self.target_pos = pygame.mouse.get_pos()
        self.target_pos_vector = pygame.math.Vector2(self.target_pos[0], self.target_pos[1])
        self.start_pos_vector = pygame.math.Vector2(self.start_x, self.start_y)
        self.angle = self.target_pos_vector - self.start_pos_vector
        self.direction = pygame.math.Vector2.normalize(self.angle)
        
        player.bulletList.append(self)
        

    def update(self):
        self.movement[0] = self.position[0] - self.rect.x
        self.movement[1] = self.position[1] - self.rect.y
        self.position += self.direction * self.speed  
        print(self.rect.x)
        print(self.rect.topleft)
        
        
        self.rect.move_ip(self.movement[0], self.movement[1])
        if self.rect.x < 0 or self.rect.x > WINDOWWIDTH or self.rect.y < 0 or self.rect.y > WINDOWHEIGHT:
            player.bulletList.remove(self)
           

#-----END CLASSES-----

pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Shoot and Prosper')
font = pygame.font.SysFont(None, 22)

playing = True


#-----TITLE LOOP-----
while playing:
    windowSurface.fill(BLACK)
    drawText('SHOOT AND PROSPER', WHITE, WINDOWWIDTH / 3, WINDOWHEIGHT / 3, windowSurface)
    pygame.display.update()
    waitForInput()
    player = Player()
    attackTimer = player.attackSpeed - 1 

    while True:

        attackTimer += 1

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
                    player.shoot()


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
                   
        #-----UPDATE INFORMATION-----
        player.update()
        for b in player.bulletList[:]:
            b.update()
        #-----DRAW INFO TO SCREEN-----
        windowSurface.fill(BLACK)    
        windowSurface.blit(player.image, player.rect)
        for b in player.bulletList[:]:
            windowSurface.blit(b.image, b.rect)
        pygame.display.update()
        clock.tick(60) 
       
windowSurface.fill(BLACK)
pygame.display.update()
