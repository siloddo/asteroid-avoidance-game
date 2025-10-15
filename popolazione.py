import player
import math
import random

class Popolazione:
    def __init__(self, numero,screen, bordo_x=1000, bordo_y=700):

        self.num_of_ships=numero
        self.screen=screen
        self.estinta=False
        self.bordo_x=bordo_x
        self.bordo_y=bordo_y
        self.best=[]
        
        self.players=[]
        for i in range(self.num_of_ships):
            self.players.append(player.Car((random.randint(100,255), random.randint(100,255),random.randint(100,255)),500,500))
        
        self.angles=[]
        for i in range(0,16):
            self.angles.append(i*math.pi/8)

    def update(self,lista_asteroidi):
        self.vivi=0
        somma_score=0
        
        numero_p=len(self.players)
        for p in self.players:
            
            if not p.alive:
                
                continue
            d_min=500
            for ast in lista_asteroidi:
                 ax = ast.x + ast.width / 2
                 ay = ast.y + ast.height / 2

                 dist = math.hypot(p.x - ax, p.y - ay)
                
                 d_min=min(dist, d_min)
                     
                 if p.collisione(ast):
                    p.score-= 200
                    p.alive=False
                    break
            
                
                    
            somma_score+=p.score
        
        
            
                    
            
            visione=[p.vision(ang, lista_asteroidi, self.screen) for ang in self.angles]
            p.think(visione)
            assert len(visione) == 16, f"vision ha {len(visione)} valori, attesi 16"
            p.update(d_min)
            
            p.draw(self.screen)
            p.borders(self.bordo_x,self.bordo_y)
            if p.alive:
                
                self.vivi+=1
        self.estinta= (self.vivi==0)
        if self.estinta:
            print(f"media score:{somma_score/numero_p}")
        

    
    
        
    def nuova_generazione_random(self):
            # rinascono tutte con cervelli nuovi (baseline semplice)
            self.players = [player.Car(
                color=(random.randint(100,255), random.randint(100,255), random.randint(100,255)),
                x=self.bordo_x//2,
                y=self.bordo_y//2
            ) for _ in range(self.num_of_ships)]
            self.estinta = False

        
    def next_generation_elitism(self, elite=2, parents_pool=10, mut_prob=0.1, mut_sigma=0.2):
        # 0) limiti sani
        elite = max(1, min(elite, self.num_of_ships))
        parents_pool = max(elite, min(parents_pool, self.num_of_ships))

        # 1) ordina SOLO la generazione corrente per score (niente Hall of Fame)
        ranked = sorted(self.players, key=lambda p: p.score, reverse=True)
        campioni = ranked[:elite]             # élite della *generazione corrente*
        genitori = ranked[:parents_pool]  
        print(f"punteggio migliore: {ranked[0].score}")    # pool di genitori della *generazione corrente*

        # 2) crea la nuova popolazione
        new_players = []

        # 2a) élite clonati (elitismo "puro")
        for p in campioni:
            clone = player.Car(color=p.color, x=self.bordo_x//2, y=self.bordo_y//2)
            clone.brain = p.brain.clone()
            # reset stato
            clone.score = 0
            clone.alive = True
            clone.velocity_x = 0
            clone.velocity_y = 0
            new_players.append(clone)

        # 2b) figli da crossover + mutate usando solo la generazione corrente
        import random
        while len(new_players) < self.num_of_ships:
            mom, dad = random.sample(genitori, 2) if len(genitori) > 1 else (genitori[0], genitori[0])
            child = player.Car(
                color=(random.randint(100,255), random.randint(100,255), random.randint(100,255)),
                x=self.bordo_x//2, y=self.bordo_y//2
            )
            child.brain = mom.brain.crossover(dad.brain)
            child.brain.mutate(prob=mut_prob, sigma=mut_sigma)

            # reset stato
            child.score = 0
            child.alive = True
            child.velocity_x = 0
            child.velocity_y = 0

            new_players.append(child)

        # 3) sostituisci popolazione + reset flag
        self.players = new_players
        self.estinta = False
