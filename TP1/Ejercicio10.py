import numpy as np
import random
import matplotlib.pyplot as plt

contagionProbability = 1
healProbability = 0.8
healSteps = 20
topMovementLimit = 100
bottomMovementLimit = 0
transmissionDistance = 2

class Particle:
    def __init__(self, x, y, isInfected, canMove, infectedSteps=0):
        self.x = x
        self.y = y
        self.isInfected = isInfected
        self.infectedSteps = infectedSteps
        self.canMove = canMove
    def isNear(self, otherParticle):
        return (otherParticle.x <= self.x + transmissionDistance and otherParticle.x >= self.x - transmissionDistance and
                otherParticle.y <= self.y + transmissionDistance and otherParticle.y >= self.y - transmissionDistance)
    def move(self):
            p = random.random()
            if (p < 0.25 and self.x + 1 < topMovementLimit):
                self.x += 1
            elif (0.25 <= p < 0.5 and self.y + 1 < topMovementLimit):
                self.y += 1
            elif (0.5 <= p < 0.75 and self.x -1 > bottomMovementLimit):
                self.x -= 1
            elif (0.75 <= p and self.y -1 > bottomMovementLimit):
                self.y -= 1
    def tryHeal(self):
        if(self.isInfected and self.infectedSteps > healSteps and random.random() <= healProbability):
            self.infectedSteps = 0
            self.isInfected = False
            self.canMove = True
        elif(self.isInfected and self.infectedSteps <= healSteps):
            self.infectedSteps += 1
    def isGotInfected(self, nNearSicks):
        isInfected = self.isInfected
        for i in range(1, nNearSicks):
            if (random.random() <= 1):
                isInfected = True
        return isInfected

    def normalMove(self, nNearSicks, heal, restricMovement):
        if(restricMovement and self.canMove or not restricMovement):
            self.move()
        if(not self.isInfected and nNearSicks > 0):
            self.isInfected = self.isGotInfected(nNearSicks)
        if(heal):
            self.tryHeal()


def getNearSickParticles(particle, otherParticles):
    nearParticles = []
    for currentParticle in otherParticles:
        if (currentParticle.isInfected and particle.isNear(currentParticle)):
            nearParticles.append(currentParticle)
    return nearParticles


def simulate(times, state, canHeal, restricMovement, showCurrentStatus):
    sickParticles, notSickParticles, ntimes = [], [], []
    for i in range(1, times):
        for j in range(0, len(state)):
            nearSickParticles = getNearSickParticles(state[j], state)
            state[j].normalMove(len(nearSickParticles), canHeal, restricMovement)
            
        sickParticles.append((len([particle for particle in state if particle.isInfected])))
        notSickParticles.append((len([particle for particle in state if not particle.isInfected])))
        ntimes.append(i)
        if(showCurrentStatus):
            plotCurrentStatus(i, state)
    plotFinalStatus(sickParticles, notSickParticles, ntimes)

def modelA1(showCurrentStatus):
    nParticles, times = 100, 4000
    initialSickPercent, initialImmobilizedPercent = 5, 0
    canHeal, restricMovement = False, False
    initialStateA1 = createInitialState(nParticles, initialSickPercent, initialImmobilizedPercent)
    simulate(times, initialStateA1, canHeal, restricMovement, showCurrentStatus)

def modelB1(showCurrentStatus):
    nParticles, times = 100, 4000
    initialSickPercent, initialImmobilizedPercent = 5, 0 
    canHeal, restricMovement = True, False
    initialStateB1 = createInitialState(nParticles, initialSickPercent, initialImmobilizedPercent)
    simulate(times, initialStateB1, canHeal, restricMovement, showCurrentStatus)

def modelA3(showCurrentStatus):
    nParticles, times = 100, 4000
    initialSickPercent, initialImmobilizedPercent = 5, 50
    canHeal, restricMovement = False, True
    initialStateA3 = createInitialState(nParticles, initialSickPercent, initialImmobilizedPercent)
    simulate(times, initialStateA3, canHeal, restricMovement, showCurrentStatus)

def modelB3(showCurrentStatus):
    nParticles, times = 100, 4000
    initialSickPercent, initialImmobilizedPercent = 5, 50 
    canHeal, restricMovement = True, True
    initialStateB3 = createInitialState(nParticles, initialSickPercent, initialImmobilizedPercent)
    simulate(times, initialStateB3, canHeal, restricMovement, showCurrentStatus)



def main():
#    modelA1(False)
#    modelB1(False)
     modelA3(False)
#    modelB3(False)


       
def createInitialState(nParticles, initialSick, intialCantMove):
    state = []
    nSick = (nParticles*initialSick)/100
    pDontMove = (intialCantMove)/100
    for i in range(0, nParticles):
        state.append(
            Particle(np.random.randint(bottomMovementLimit,topMovementLimit),
                     np.random.randint(bottomMovementLimit, topMovementLimit),
                     i < nSick,
                     random.random() > pDontMove))
    return state

    
def plotCurrentStatus(currentTime, currentState):
    plt.cla()
    plt.scatter(list(map(getXSick, currentState)), list(map(getYSick, currentState)), color='green', label='times:  %.1f' %(currentTime))
    plt.scatter(list(map(getXNotSick, currentState)), list(map(getYNotSick, currentState)), color='black')
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, loc='upper center')
    plt.pause(0.00001)

def plotFinalStatus(sickParticles, notSickParticles, ntimes):
    plt.plot(ntimes, sickParticles, color='green', label='Infectados')
    plt.plot(ntimes, notSickParticles, color='blue', label='Sanos')
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
    plt.show()

def getXSick(p):
    if(p.isInfected):
        return p.x
def getYSick(p):
    if(p.isInfected):
        return p.y
def getXNotSick(p):
    if(not p.isInfected):
        return p.x
def getYNotSick(p):
    if(not p.isInfected):
        return p.y


if __name__ == "__main__":
    main()






