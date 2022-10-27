from statistics import mean
import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

######################################################################################################################################################
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

        out = []

        for index in self.blue:
            out.append(self.vertices[index].jump(self,beta))

        for index in self.red:
            out.append(self.vertices[index].jump(self,beta))

        self.state_history.extend(out)
        return(out)

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
        
       
        jmp_prob=1/(math.exp(-2*beta*spin_bias) + 1)

        #print(jmp_prob)

        if jmp_prob>np.random.random():
            self.spin = 1
        else:
            self.spin = -1

        return(self.spin)
###########################################################################################################################################################
        

        

test = Issing(100)

beta = 0.44
num_iterations = 1000
plot_y = [1]
count = 1
while count <= num_iterations:
    test.step(beta)
    plot_y.append(mean(test.current_state()))
    count = count + 1
    if count%(num_iterations/100) == 0:
                print((count/num_iterations)*100,"%")


plot_x = np.arange(0,num_iterations+1,1)
plot_y = np.array(plot_y)
plt.plot(plot_x, plot_y, color = 'Red')
m_inf = (1-math.sinh(2*beta)**-4)**(1/8)

plt.axhline(m_inf.real)
plt.axhline(mean(test.state_history), color = 'red')

plt.show()