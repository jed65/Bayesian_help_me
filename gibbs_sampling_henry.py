import numpy as np
import math
import cmath
import matplotlib.pyplot as plt

#My implementation of a Gibbs Sampler for use withe the Ising Model.
# It is implemented as 2 Classes.

######################################################################################################################################################

#This class is where the main computations take place
class Issing:

    def __init__(self,n):
        self.size=n**2
        self.vertices = [] #A list that contains the the vertices
        self.blue = [] #Lists which contains teh blue and red vertices
        self.red = []
        self.state_history = np.ones(self.size).tolist() #A vector which conatins the current and history of the states of the vertices.

        count = 0
        #Initialising each vertice
        while count < self.size:
            self.vertices.append(Vertex(count,n))
            count = count + 1

        #Creating the lsit of Blur and Red vertices
        if n%2 == 1: #Odd case
            self.blue.extend(np.arange(0,self.size,2).tolist())
            self.red.extend(np.arange(1,self.size,2).tolist())
        else: #Even Case
            count = 0
            while count < n:
                if count%2 == 0:
                    self.blue.extend(np.arange(count*n,(count+1)*n,2).tolist())
                    self.red.extend(np.arange(count*n+1,(count+1)*n,2).tolist())
                else:
                    self.blue.extend(np.arange(count*n+1,(count+1)*n,2).tolist())
                    self.red.extend(np.arange(count*n,(count+1)*n,2).tolist())
                
                count = count + 1

    #A functio  which completes a step using gibbs sampling
    def step(self,beta):

        out = []

        #First the blue points
        for index in self.blue:
            out.append(self.vertices[index].jump(self,beta))

        #Second the Red
        for index in self.red:
            out.append(self.vertices[index].jump(self,beta))

        #Extend state_history with new states
        self.state_history.extend(out)
        return(self.state_history)

    #A function the returns the current state of the vertices
    def current_state(self):
        out = []
        for index in np.arange(0,self.size,1):
            out.append(self.vertices[index].spin)
        return(out)

    #The main function to be called when creating a sample using Gibbs sampling
    def giibbs_sample(self,beta,num_iterations):
        count = 0
        while count < num_iterations: #Step for each iteration
            self.step(beta)
            count = count + 1
            if count%(num_iterations/100) == 0: #Print the completion progress
                print((count/num_iterations)*100,"%")
        
        return np.mean(self.state_history)


#############################################################################################################################################
#A class which contains information and methods for the vertices.
class Vertex:

    def __init__(self,location,n):
        self.location = location #Location in the grid
        self.spin = 1 #Current state
        self.neighbors = [] #Neighboring points.

        #Setting up the neighboring points
        if location%n != 0: 
            self.neighbors.append(location - 1)
        
        if location%n != n-1:
            self.neighbors.append(location + 1)

        if location >= n:
            self.neighbors.append(location - n)

        if location + 1 <=n*(n-1):
            self.neighbors.append(location + n)
        
        
    #Jump the vertex to the next state depending on its neighbors
    def jump(self,grid,beta):
        spin_bias = 0

        #Grabs the spins of neighbors
        for index in self.neighbors:
            spin_bias = spin_bias + grid.vertices[index].spin
        
        #Probability of changing state       
        jmp_prob=1/(math.exp(-2*beta*spin_bias) + 1)

        #Grabbing a random number from the uniform distribution between -1,1
        if jmp_prob>np.random.random():
            self.spin = 1
        else:
            self.spin = -1

        return(self.spin)
###########################################################################################################################################################
        

        
#Testing out are model
test = Issing(100) #Creating are Grid

beta = 0.43
num_iterations = 10000

#Ploting the output
plot_y = [1]
count = 1
while count <= num_iterations:
    test.step(beta)
    plot_y.append(np.mean(test.current_state()))
    count = count + 1
    if count%(num_iterations/100) == 0:
                print((count/num_iterations)*100,"%")


plot_x = np.arange(0,num_iterations+1,1)
plot_y = np.array(plot_y)
plt.plot(plot_x, plot_y, color = 'Red')
m_inf = (1-math.sinh(2*beta)**-4)**(1/8)

plt.axhline(m_inf.real)
plt.axhline(np.mean(test.state_history), color = 'red')

plt.show()
