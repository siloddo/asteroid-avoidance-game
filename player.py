import pygame
import random
import nodo
import math
class Car:
    def __init__(self,color, x=100,y=100,width=35, height=35):
        self.border_cooldown=10
        self.brain=nodo.Brain(16,14,4)
        self.velocity=3
        self.alive=True
        self.x=x
        self.y=y
        self.width=width
        self.alive=True
        self.velocity_y=0
        self.velocity_x=0
        self.height=height
        self.color=color
        self.score=0

    def draw(self, screen):
        if self.alive:
        
            pygame.draw.rect(screen, self.color, (self.x,self.y, self.width, self.height))
    def manuale (self, key, incremento=0.003):
         if key[pygame.K_LEFT]:
            self.velocity_x-=incremento
         if key[pygame.K_RIGHT]:
            
            self.velocity_x+=incremento
         if key[pygame.K_UP]:
            
            self.velocity_y-=incremento
            
            
         if key[pygame.K_DOWN]:
            self.velocity_y+=incremento

         
         
         
    def update(self, d_min):
        visione=[]
        
        if self.alive:
             
            self.x+=self.velocity_x
            self.y+=self.velocity_y
            if self.velocity_y>5:
                    self.velocity_y=5
            if self.velocity_x>5:
                    self.velocity_x=5
            if self.velocity_y<-5:
                    self.velocity_y=-5
            if self.velocity_x<-5:
                    self.velocity_x=-5

            self.score+=1
                                # +1 per frame vivo
            self.score += 0.01 * d_min           # bonus stare lontano (scala a piacere)
            self.score -= 10 * (abs(self.velocity_x)+abs(self.velocity_y) < 0.1)  # punisci stare fermo
            
        
            
            
             

    def borders(self, bordo_x, bordo_y):
        if self.border_cooldown > 0:
            self.border_cooldown -= 1

        hit = False
        if self.x > bordo_x - self.width:
            self.x = bordo_x - self.width
            hit = True
        if self.y >= bordo_y-self.height:
            self.y = bordo_y-self.height
            hit = True
        if self.x < 0:
            self.x = 0
            hit = True
        if self.y < 0:
            self.y = 0
            hit = True

        if hit:
            self.score -= 30000        # penalità singola
        # facoltativo: rimbalzo/damping per “staccarli” dal bordo
            self.velocity_x *= -0.3
            self.velocity_y *= -0.3
            self.border_cooldown = 10  # ~10 frame di “invulnerabilità” al bordo
            self.alive=False

    def collisione(self, asteroide):
        rect_car = pygame.Rect(self.x, self.y, self.width, self.height)
        rect_ast = pygame.Rect(asteroide.x, asteroide.y, asteroide.width, asteroide.height)
        if rect_car.colliderect(rect_ast):
             self.alive=False
        return rect_car.colliderect(rect_ast)
    
    
    def vision(self, angle, asteroidi, screen, distanza_max=500, disegna=False):
        
        ox = self.x + self.width // 2
        oy = self.y + self.height // 2

    # precomputo direzione
        dx = math.cos(angle)
        dy = math.sin(angle)

        ex = ox + dx * distanza_max
        ey = oy + dy * distanza_max

        # trova l’asteroide più vicino che interseca il segmento (ox,oy)-(ex,ey)
        min_d = distanza_max
        hit_end = (ex, ey)

        for ast in asteroidi:
            r = pygame.Rect(ast.x, ast.y, ast.width, ast.height)
            #clipped è il segmento tra le due coppie di punti
            clipped = r.clipline((ox, oy), (ex, ey))  # se intersecano, restituisce il segmento tagliato
            if clipped:
                # clipped è ((ix1,iy1),(ix2,iy2)); scegli il punto più vicino all’origine
                (ix1, iy1), (ix2, iy2) = clipped
                # prendi il punto “ingresso”
                ix, iy = (ix1, iy1) if (ix1-ox)**2 + (iy1-oy)**2 <= (ix2-ox)**2 + (iy2-oy)**2 else (ix2, iy2)
                d = math.hypot(ix - ox, iy - oy)
                if d < min_d:
                    min_d = d
                    hit_end = (ix, iy)
        rect_world = screen.get_rect()                     # rettangolo: (0,0,w,h)
        clipped_w = rect_world.clipline((ox, oy), (ex, ey))
        if clipped_w:
            (wx1, wy1), (wx2, wy2) = clipped_w
            # scegli l’estremo che NON è l'origine (ox,oy): è il punto d'impatto col muro
            d1 = (wx1 - ox)**2 + (wy1 - oy)**2
            d2 = (wx2 - ox)**2 + (wy2 - oy)**2
            wx, wy = (wx1, wy1) if d1 > d2 else (wx2, wy2)   # quello più lontano dall'origine (l'altro è ~0)
            d_wall = math.hypot(wx - ox, wy - oy)
            if d_wall < min_d:
                min_d = d_wall
                hit_end = (wx, wy)

        if disegna and self.alive:
            pygame.draw.line(screen, (255, 255, 0), (ox, oy), hit_end, 2)

        return min_d
    
    def think(self, visione, incremento=0.3):
         if self.alive:
            self.lista_movimenti=self.brain.feed_foward(visione)
            if self.lista_movimenti[0]>0.55:
                
                self.velocity_x-=incremento

            if self.lista_movimenti[1]>0.55:
                
                self.velocity_x+=incremento
            if self.lista_movimenti[2]>0.55:
                
                self.velocity_y-=incremento
            if self.lista_movimenti[3]>0.55:
                
                self.velocity_y+=incremento
         ax = self.lista_movimenti[1] - self.lista_movimenti[0]  # destra - sinistra
         ay = self.lista_movimenti[3] - self.lista_movimenti[2]  # giù - su
         k  = 0.3
         self.velocity_x += k * (ax - 0.5)
         self.velocity_y += k * (ay - 0.5)
         self.velocity_x *= 0.85
         self.velocity_y *= 0.85


            


              
         
         
         

                

         

         
            
              
            
        
        
        




