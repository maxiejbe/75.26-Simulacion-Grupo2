import numpy as np
import matplotlib.pyplot as plt

class Particle:
    def __init__(self, x, y, isSick, sickSteps):
        self.x = x
        self.y = y
        self.isSick = isSick
        self.sickSteps = sickSteps
    def printPosition(self):
        print(str(self.x), str(self.y), str(self.isSick))
    def isNear(self, otherParticle):
        return (otherParticle.x < self.x + 2 and otherParticle.x > self.x - 2 and
                otherParticle.y < self.y + 2 and otherParticle.y > self.y - 2)
    def move(self):
        nNearSicks = 0
        p = np.random.rand()
        if p < 0.25:
            self.x += 1
        elif 0.25 <= p < 0.5:
            self.y += 1
        elif 0.5 <= p < 0.75:
            self.x -= 1
        elif 0.75 <= p:
            self.y -= 1
        if( nNearSicks > 0):
            self.isSick = np.random.rand() > 0.6
        
   
def createInitialState(nParticles, maxPosition, initialSick):
    state = []
    nSick = (nParticles*initialSick)/100
    for i in range(0, nParticles):
        state.append(Particle(np.random.randint(1, maxPosition),np.random.randint(1, maxPosition),i < nSick,0))
    return state;

def getNearSickParticles(particle, otherParticles):
    nearParticles = []
    for currentParticle in otherParticles:
        if (currentParticle.isSick and particle.isNear(currentParticle)):
            nearParticles.append(currentParticle)
    return nearParticles

def simulate(times, nParticles, maxPosition, initialSickPercent):
    state = createInitialState(nParticles, maxPosition, initialSickPercent)
    for i in range(1, times):
        for j in range(0, len(state)):
            # nearSickParticles = getNearSickParticles(state[j], state)
            state[j].move()
        print('-----')
        state[0].printPosition()
    return state
 

def main():
    nParticles, maxPosition, times, initialSickPercent = 1, 100, 100, 100
    newState = simulate(times, nParticles, maxPosition, initialSickPercent)
    

if __name__ == "__main__":
    main()






