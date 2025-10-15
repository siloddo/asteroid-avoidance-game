import pygame
import player
import math
import asteroidi
import popolazione as pop

pygame.init()
bordo_x=1000
bordo_y=700
# Set up the display
screen=pygame.display.set_mode((bordo_x, bordo_y))
pygame.display.set_caption("My Game")
mycar=player.Car((255,255,100)
)
# Main game loop
clock=pygame.time.Clock()
def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            return False
            
    return True
def nave_manuale(keys, lista_asteroidi, angles, bordox, bordoy, visione=[]):
    for i in range(len(angles)):
            visione=[mycar.vision(ang, lista_asteroidi, screen, disegna=True) for ang in angles]
            

           # mycar.think(visione)
            
            mycar.manuale(keys)
            mycar.update(3)
            
            
            mycar.draw(screen)
            mycar.borders(bordo_x,bordo_y)
            
            
    

def main():
    generazione=0
    velocizzatore=False
    ast_cd=15
    angles=[((math.pi)/8)*i for i in range(0,16)]
    print(angles)
    
    popolazione=pop.Popolazione(20, screen)
    spawn_countdown=10
    accelleratore=0
    lista_asteroidi=[]
    tempo=60
    clock.tick(tempo)

    
    running=True
    botton_countdown=10
    while running:
        #if not mycar.alive:
        #    clock.tick(60)

        #else: 
          #  tempo-=1
         #   if tempo<30:
          #      tempo=30
         #   clock.tick(tempo)

        


       


        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            mycar.alive=True

            

        
        screen.fill((0, 0, 0))
        botton_countdown-=1
        if keys[pygame.K_q] and botton_countdown<=0 and velocizzatore==False :
            velocizzatore=True


            
        elif  keys[pygame.K_a] and botton_countdown<=0 and velocizzatore==True:
                velocizzatore=False
        
        if velocizzatore:
            clock.tick(500)
        else:
            clock.tick(60)

        


            

        if keys[pygame.K_p] and botton_countdown<=0:
            botton_countdown=10
            ast_cd-=1
            print(f"countdown spawn {ast_cd}")
        elif keys[pygame.K_l] and botton_countdown<=0:
            botton_countdown=10
            ast_cd+=1
        
            print( f"countdown spawn {ast_cd}")
        if ast_cd+15<3:
            ast_cd=0
        
        spawn_countdown-=1
        if spawn_countdown<=0:
            spawn_countdown=ast_cd
            if ast_cd<3:
                ast_cd=3
            
            
            lista_asteroidi.append(asteroidi.Asteroidi(bordo_x,bordo_y))

            
        if lista_asteroidi:
            for ast in lista_asteroidi:
                
                ast.draw(screen)
                ast.update()
                if ast.elimina():
                    lista_asteroidi.remove(ast)
               
                mycar.collisione(ast)

            nave_manuale(keys, lista_asteroidi, angles, bordo_x, bordo_y)
            popolazione.update(lista_asteroidi)
            if popolazione.estinta:
                accelleratore=0
               # prob-=0.005
               # if prob<=0.5:
                 #   prob=0.5
                popolazione.next_generation_elitism(elite=2, mut_prob=0.1, mut_sigma=0.2)
                lista_asteroidi.clear()
                generazione+=1
                print(f"generazione num:{generazione}")
                
        
        #print(mycar.score)
            
            
            
            
        

        pygame.display.update()
        running= quit_game() 
    pygame.quit()

main()