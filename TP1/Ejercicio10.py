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
    def isNear(self, otherParticle):
        return (otherParticle.x <= self.x + 2 and otherParticle.x >= self.x - 2 and
                otherParticle.y <= self.y + 2 and otherParticle.y >= self.y - 2)
    def move(self, check):
        if(check and self.canMove or not check):
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
            self.canMove = True
        elif(self.isSick and self.sickSteps < healSteps):
            self.sickSteps += 1
    def gotIt(self, nNearSicks):
        spread = False
        for i in range(1, nNearSicks):
            if (np.random.rand() < 0.6):
                spread = True
        return spread
    def normalMove(self, nNearSicks, canHeal, canRestricMovement):
        self.move(canRestricMovement)
        if(not self.isSick and nNearSicks > 0):
            self.isSick = self.gotIt(nNearSicks)
        if(canHeal):
            self.tryHeal()
        if(self.isSick):
            self.canMove = False

        

def getNearSickParticles(particle, otherParticles):
    nearParticles = []
    np.random.rand() <= healProbability
    for currentParticle in otherParticles:
        if (currentParticle.isSick and particle.isNear(currentParticle)):
            nearParticles.append(currentParticle)
    return nearParticles
def getXSick(p):
    if(p.isSick):
        return p.x
def getYSick(p):
    if(p.isSick):
        return p.y
def getXNotSick(p):
    if(not p.isSick):
        return p.x
def getYNotSick(p):
    if(not p.isSick):
        return p.y
def simulate(times, state, canHeal, canRestricMovement):
    sickParticles, notSickParticles, ntimes = [], [], []
    for i in range(1, times):
        for j in range(0, len(state)):
            nearSickParticles = getNearSickParticles(state[j], state)
            state[j].normalMove(len(nearSickParticles), canHeal, canRestricMovement)
        #sickParticles.append((len([particle for particle in state if particle.isSick])))
        #notSickParticles.append((len([particle for particle in state if not particle.isSick])))
        #ntimes.append(i)    
        plt.cla()
        plt.scatter(list(map(getXSick, state)), list(map(getYSick, state)), color='green', label='times:  %.1f' %(i))
        plt.scatter(list(map(getXNotSick, state)), list(map(getYNotSick, state)), color='black')
        plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, loc='upper center')
        plt.pause(0.001)
    plt.show()


#    plt.plot(ntimes, sickParticles, color='green', label='Infectados')
#    plt.plot(ntimes, notSickParticles, color='blue', label='Sanos')
#    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
#    plt.show()
    return state
 
   
def createInitialState(nParticles, initialSick, intialCantMove):
    state = []
    nSick = (nParticles*initialSick)/100
    pDontMove = (intialCantMove)/100
    for i in range(0, nParticles):
        state.append(
            Particle(np.random.randint(bottomMovementLimit,topMovementLimit),
                     np.random.randint(bottomMovementLimit, topMovementLimit),
                     i < nSick,
                     np.random.rand() > pDontMove))
    return state


def modelA1():
    nParticles, times = 100, 4000
    initialSickPercent, initialImmobilizedPercent = 5, 0
    stateA1 = createInitialState(nParticles, initialSickPercent, initialImmobilizedPercent)
    simulate(times, stateA1, False, False)

def modelB1():
    nParticles, times = 100, 4000
    initialSickPercent, initialImmobilizedPercent = 5, 0 
    stateA1 = createInitialState(nParticles, initialSickPercent, initialImmobilizedPercent)
    simulate(times, stateA1, True, False)



def main():
#   modelA1()
    modelB1()


    
    

if __name__ == "__main__":
    main()






