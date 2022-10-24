from statistics import mean
import numpy as np
import math
import random

class Issing:

    def __init__(self,n):
        self.size=n**2
        self.vertices = []
        self.blue = []
        self.red = []
        self.state_history = np.ones(self.size).tolist()

        count = 0
        while count < self.size:
            self.vertices.append(Vertex(count,n))
            count = count + 1

        if n%2 == 1:
            self.blue.extend(np.arange(0,self.size,2).tolist())
            self.red.extend(np.arange(1,self.size,2).tolist())
        else:
            count = 0
            while count < n:
                if count%2 == 0:
                    self.blue.extend(np.arange(count*n,(count+1)*n,2).tolist())
                    self.red.extend(np.arange(count*n+1,(count+1)*n,2).tolist())
                else:
                    self.blue.extend(np.arange(count*n+1,(count+1)*n,2).tolist())
                    self.red.extend(np.arange(count*n,(count+1)*n,2).tolist())
                
                count = count + 1

    def step(self,beta):

        for index in self.blue:
            self.state_history.append(self.vertices[index].jump(self,beta))

        for index in self.red:
            self.state_history.append(self.vertices[index].jump(self,beta))

    def current_state(self):
        out = []
        for index in np.arange(0,self.size,1):
            out.append(self.vertices[index].spin)
        return(out)

    def giibbs_sample(self,beta,num_iterations):
        count = 0
        while count < num_iterations:
            self.step(beta)
            count = count + 1
            if count%(num_iterations/100) == 0:
                print((count/num_iterations)*100,"%")
        
        return mean(self.state_history)


#############################################################################################################################################
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

        if location + 1 <=n*(n-1):
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

        return(self.spin)
###########################################################################################################################################################
        

        

test = Issing(100)

beta = 1

print(test.giibbs_sample(beta,1000))