import numpy as np
import matplotlib.pyplot as plt

contagionProbability = 1
healProbability = 0.8
healSteps = 20
topMovementLimit = 100
bottomMovementLimit = 0

class Particle:
    def __init__(self, x, y, isSick, canMove, sickSteps=0):
        self.x = x
        self.y = y
        self.isSick = isSick
        self.sickSteps = sickSteps
        self.canMove = canMove
    def printPosition(self):
        print(str(self.x), str(self.y), str(self.isSick), str(self.sickSteps))
    def isNear(self, otherParticle):
        return (otherParticle.x <= self.x + 2 and otherParticle.x >= self.x - 2 and
                otherParticle.y <= self.y + 2 and otherParticle.y >= self.y - 2)
    def move(self):
        p = np.random.rand()
        if (p < 0.25 and self.x + 1 < topMovementLimit):
            self.x += 1
        elif (0.25 <= p < 0.5 and self.y + 1 < topMovementLimit):
            self.y += 1
        elif (0.5 <= p < 0.75 and self.x -1 > bottomMovementLimit):
            self.x -= 1
        elif (0.75 <= p and self.y -1 > bottomMovementLimit):
            self.y -= 1
    def tryHeal(self):
        if(self.isSick and self.sickSteps >= healSteps and np.random.rand() <= healProbability):
            self.sickSteps = 0
            self.isSick = False
        elif(self.isSick and self.sickSteps < healSteps):
            self.sickSteps += 1

    def normalMove(self, nNearSicks, canHeal):
        if(self.canMove):
            self.move()
        if(not self.isSick and nNearSicks > 0 and np.random.rand() <= contagionProbability):
            self.isSick = True
        if(canHeal):
            self.tryHeal()

    def notSickMove(self, nNearSicks, canHeal):
        if(not self.isSick):
            self.move()
        if(not self.isSick and nNearSicks > 0 and np.random.rand() <= contagionProbability):
            self.isSick = True
        if(canHeal):
            self.tryHeal()
        
   
def createInitialState(nParticles, initialSick, particleMovePercentage):
    state = []
    nSick = (nParticles*initialSick)/100
    nMove = (nParticles * particleMovePercentage)/100
    for i in range(0, nParticles):
        state.append(Particle(np.random.randint(bottomMovementLimit, topMovementLimit),np.random.randint(bottomMovementLimit, topMovementLimit),i < nSick,i < nMove))
    return state;

def getNearSickParticles(particle, otherParticles):
    nearParticles = []
    for currentParticle in otherParticles:
        if (currentParticle.isSick and particle.isNear(currentParticle)):
            nearParticles.append(currentParticle)
    return nearParticles

def simulate(times, state, canHeal):
    sickParticles = []
    notSickParticles = []
    ntimes = []
    for i in range(1, times):
        for j in range(0, len(state)):
            nearSickParticles = getNearSickParticles(state[j], state)
            state[j].normalMove(len(nearSickParticles), canHeal)
        sickParticles.append((len([particle for particle in state if particle.isSick])))
        notSickParticles.append((len([particle for particle in state if not particle.isSick])))
        ntimes.append(i)

    plt.plot(ntimes, sickParticles)
    plt.plot(ntimes, notSickParticles)
    plt.show()
    return state
 


def modelA1():
    nParticles, times = 100, 4000
    initialSickPercent, particleMovePercentage = 5, 100 
    stateA1 = createInitialState(nParticles, initialSickPercent, particleMovePercentage)
    simulate(times, stateA1, False)

def modelA3():
    nParticles, times = 100, 4000
    initialSickPercent, particleMovePercentage = 5, 50 
    stateA1 = createInitialState(nParticles, initialSickPercent, particleMovePercentage)
    simulate(times, stateA1, False)

def modelB1():
    nParticles, times = 100, 1000
    initialSickPercent, particleMovePercentage = 5, 100 
    stateA1 = createInitialState(nParticles, initialSickPercent, particleMovePercentage)
    simulate(times, stateA1, True)

def modelB3():
    nParticles, times = 100, 1000
    initialSickPercent, particleMovePercentage = 5, 50 
    stateA1 = createInitialState(nParticles, initialSickPercent, particleMovePercentage)
    simulate(times, stateA1, True)

def main():

    modelA1()
#    modelA2()
    modelA3()
    modelB1()
#    modelB2()
    modelB3()


    
    

if __name__ == "__main__":
    main()






