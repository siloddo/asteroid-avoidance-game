import random
import pygame
import math

class Asteroidi:

    def __init__(self, bordo_x,bordo_y):
        
        self.bordo_x=bordo_x
        self.bordo_y=bordo_y
        self.maxvelocity=3
        self.min_velocity=2
        self.velocity_x=0
        self.velocity_y=0
        
        self.aggiungi=0.9
        self.x=0
        self.y=0
        
            

        
        
        
        self.color =(255, 128, 128)
        self.width=30
        self.height=30
        speed = random.uniform(self.min_velocity, self.maxvelocity)

        
        lato=random.randint(0,3)
        if lato == 0:  # sinistra
            self.x = 0
            self.y = random.randint(0, bordo_y - self.height)
        elif lato == 1:  # basso
            self.x = random.randint(0, bordo_x - self.width)
            self.y = bordo_y - self.height
        elif lato == 2:  # alto
            self.x = random.randint(0, bordo_x - self.width)
            self.y = -self.height
        elif lato == 3:  # destra
            self.x = bordo_x - self.width
            self.y = random.randint(0, bordo_y - self.height)

        tx = random.uniform(0, bordo_x)
        ty = random.uniform(0, bordo_y)

        dx = tx - (self.x + self.width / 2)
        dy = ty - (self.y + self.height/2)
        dist = math.hypot(dx, dy) or 1.0
        self.velocity_x = (dx / dist) * speed
        self.velocity_y = (dy / dist) * speed

        
            
            
             


    def draw(self, screen):
        
        pygame.draw.rect(screen, self.color, (self.x,self.y, self.width, self.height))
    def update(self):
        self.x+=self.velocity_x
        self.y+=self.velocity_y
    def elimina(self):
        if self.x>self.bordo_x:
            return True
        elif self.x<0:
            return True
        elif self.y>self.bordo_y:
            return True
        elif self.y<0:
            return True
        return False



        