import random
import math
class Node:
    def __init__(self, id, layer):
        self.id=id
        self.layer=layer
        self.output=0
        self.bias=0
        self.input=0

class Connection:
    def __init__(self, from_node, to_node, weight):
        self.from_node=from_node
        self.to_node=to_node
        self.weight=weight
        
        

class Brain:
    def __init__(self, input, hidden, output):
        self.nodi=[]
        self.input=input
        self.output=output
        self.hidden=hidden
        self.weight=[]
        self.bias=0
        for i in range(input):
            self.nodi.append(Node(i,0))
        for i in range(hidden):
            self.nodi.append(Node(i,1))
        for i in range(output):
            self.nodi.append(Node(i,2))
        
        self.connessioni=[]

        for input_node in self.nodi:
            for output_node in self.nodi:
                
                if output_node.layer  == input_node.layer+1:
                    peso=random.uniform(-1,1)
                    self.weight.append(peso)
                    self.connessioni.append(Connection(input_node,output_node, peso))
        for n in self.nodi:
            if n.layer in (1,2):
                n.bias=random.uniform(-1,1)
                

    def sigmoid(self,x):
        return 1/(1+math.exp(-x))
    
    def clone(self):
        child = Brain(self.input, self.hidden, self.output)
        for i, con in enumerate(self.connessioni):
            child.connessioni[i].weight = con.weight
        for n_child, n in zip(child.nodi, self.nodi ):
            n_child.bias=n.bias
        return child
    def mutate(self, prob=0.3, sigma=0.1):
        for con in self.connessioni:
            if random.random()>prob:
                con.weight+=random.gauss(0,sigma)
        #bias
        for n in self.nodi:
            if n.layer in (1, 2) and random.random() < prob:
                n.bias += random.gauss(0, sigma)
    def crossover(self, other):
        child = Brain(self.input, self.hidden, self.output)
        for i, con in enumerate(child.connessioni):
            # uniform crossover
            con.weight = (self.connessioni[i].weight
                        if random.random() < 0.5
                        else other.connessioni[i].weight)
        for i, n_child in enumerate(child.nodi):
            if n_child.layer in (1, 2):
                if random.random() < 0.5:
                    n_child.bias = self.nodi[i].bias      # dal genitore A
                else:
                    n_child.bias = other.nodi[i].bias   

        return child
    

    def feed_foward(self,vision):
        for i in range(self.input):
            self.nodi[i].output=vision[i]/500
        
        for nodo in self.nodi:
            if nodo.layer==1:
                somma=0
                for con in self.connessioni:
                    if con.to_node==nodo:
                        somma+=con.from_node.output*con.weight

                somma+=nodo.bias  
                nodo.output=self.sigmoid(somma)
        for nodo in self.nodi:
            if nodo.layer == 2:  # output layer
                somma = 0
                for con in self.connessioni:
                    if con.to_node == nodo:
                        somma += con.from_node.output * con.weight
                somma+=nodo.bias  
                nodo.output = self.sigmoid(somma)
        return [n.output for n in self.nodi if n.layer==2]
rete = Brain(16, 14, 4)




            
            
            


                
