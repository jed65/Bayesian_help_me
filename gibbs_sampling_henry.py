import numpy as np
import math
import random

class Issing:

    def __init__(self,n):
        self.size=n**2
        self.vertices = []

        count = 0
        while count < self.size:
            self.vertices.append(Vertex(count,n))
            count = count + 1

    def step(self,beta):

        if self.size%2==0:
            a=1

        else:
            for index in np.arange(0,self.size-1,2).tolist():
                self.vertices[index].jump(self,beta)

            for inde in np.arange(0,self.size-1,2).tolist():
                self.vertices[index].jump(self,beta)

        
class Vertex:

    def __init__(self,location,n):
        self.location = location
        self.spin = 1
        self.negibours = []

        if location%n != 0: 
            self.negibours.append(location - 1)
        
        if location%n != n-1:
            self.negibours.append(location + 1)

        if location >= n:
            self.negibours.append(location - n)

        if location <=n*(n-1):
            self.negibours.append(location + n)
        
        
    
    def jump(self,grid,beta):
        spin_bias = 0

        for index in self.negibours:
            spin_bias = spin_bias + grid.vertices[index].spin
        
       
        jmp_prob=(math.exp(4*beta*spin_bias) + 1)/(2*(math.cosh(4*beta*spin_bias)+1))

        #print(jmp_prob)

        if jmp_prob>random.randint(0,1):
            self.spin = 1
        else:
            self.spin = -1

        

        

test = Issing(3)

print(test.size)
print(test.vertices[0].negibours)
beta=0.44
test.vertices[4].jump(test,beta)

test.step(beta)