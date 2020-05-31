import numpy as np
import random
import matplotlib.pyplot as plt

contagionProbability = 1
heal_probability = 0.8
heal_steps = 20
top_movement_limit = 100
bottom_movement_limit = 0
transmission_distance = 2
steps_until_not_move = 10

class Particle:
    def __init__(self, x, y, is_infected, can_move, infected_steps=0):
        self.x = x
        self.y = y
        self.is_infected = is_infected
        self.infected_steps = infected_steps
        self.can_move = can_move
    def isNear(self, other_particle):
        return (other_particle.x <= self.x + transmission_distance and other_particle.x >= self.x - transmission_distance and
                other_particle.y <= self.y + transmission_distance and other_particle.y >= self.y - transmission_distance)
    def move(self):
        p = random.random()
        if (p < 0.25 and self.x + 1 < top_movement_limit):
            self.x += 1
        elif (0.25 <= p < 0.5 and self.y + 1 < top_movement_limit):
            self.y += 1
        elif (0.5 <= p < 0.75 and self.x -1 > bottom_movement_limit):
            self.x -= 1
        elif (0.75 <= p and self.y -1 > bottom_movement_limit):
            self.y -= 1
    def tryHeal(self):
        if(self.is_infected and self.infected_steps > heal_steps and random.random() <= heal_probability):
            self.is_infected = False
            self.can_move = True
        elif(self.is_infected and self.infected_steps <= heal_steps):
            self.infected_steps += 1
    def isGotInfected(self, nNearSicks):
        is_infected = self.is_infected
        for i in range(1, nNearSicks):
            if (random.random() <= 1):
                is_infected = True
        return is_infected

    def normalMove(self, nNearSicks, heal, restric_movement, infectedCantMove):
        if(restric_movement and self.can_move or not restric_movement):
            self.move()
        if(not self.is_infected and nNearSicks > 0):
            self.is_infected = self.isGotInfected(nNearSicks)
        if(heal):
            self.tryHeal()
        print(infectedCantMove, self.is_infected, self.infected_steps, steps_until_not_move, self.infected_steps > steps_until_not_move)
        if(infectedCantMove and self.is_infected and self.infected_steps > steps_until_not_move):
            print('alguno deberia dejar de moverse')
            self.can_move = False


def getNearSickParticles(particle, other_particles):
    nearParticles = []
    for currentParticle in other_particles:
        if (currentParticle.is_infected and particle.isNear(currentParticle)):
            nearParticles.append(currentParticle)
    return nearParticles


def simulate(times, state, can_heal, restric_movement, showCurrentStatus, infectedCantMove = False):
    sickParticles, notSickParticles, ntimes = [], [], []
    for i in range(1, times):
        for j in range(0, len(state)):
            nearSickParticles = getNearSickParticles(state[j], state)
            state[j].normalMove(len(nearSickParticles), can_heal, restric_movement, infectedCantMove)
            
        sickParticles.append((len([particle for particle in state if particle.is_infected])))
        notSickParticles.append((len([particle for particle in state if not particle.is_infected])))
        ntimes.append(i)
        if(showCurrentStatus):
            plotCurrentStatus(i, state)
    plotFinalStatus(sickParticles, notSickParticles, ntimes)

def modelA1(showCurrentStatus):
    n_particles, times = 100, 4000
    initial_sick_percent, initial_immobilized_percent = 5, 0
    can_heal, restric_movement = False, False
    initial_State_A1 = createInitialState(n_particles, initial_sick_percent, initial_immobilized_percent)
    simulate(times, initial_State_A1, can_heal, restric_movement, showCurrentStatus)

def modelB1(showCurrentStatus):
    n_particles, times = 100, 4000
    initial_sick_percent, initial_immobilized_percent = 5, 0 
    can_heal, restric_movement = True, False
    initial_state_B1 = createInitialState(n_particles, initial_sick_percent, initial_immobilized_percent)
    simulate(times, initial_state_B1, can_heal, restric_movement, showCurrentStatus)

def modelA3(showCurrentStatus):
    n_particles, times = 100, 4000
    initial_sick_percent, initial_immobilized_percent = 5, 50
    can_heal, restric_movement = False, True
    initial_state_A3 = createInitialState(n_particles, initial_sick_percent, initial_immobilized_percent)
    simulate(times, initial_state_A3, can_heal, restric_movement, showCurrentStatus)

def modelB3(showCurrentStatus):
    n_particles, times = 100, 4000
    initial_sick_percent, initial_immobilized_percent = 5, 50 
    can_heal, restric_movement = True, True
    initial_state_B3 = createInitialState(n_particles, initial_sick_percent, initial_immobilized_percent)
    simulate(times, initial_state_B3, can_heal, restric_movement, showCurrentStatus)

def modelA2(showCurrentStatus):
    n_particles, times = 100, 300
    initial_sick_percent, initial_immobilized_percent = 5, 0
    can_heal, restric_movement, infectedCantMove = False, True, True
    initial_State_A1 = createInitialState(n_particles, initial_sick_percent, initial_immobilized_percent)
    simulate(times, initial_State_A1, can_heal, restric_movement, showCurrentStatus, infectedCantMove)

def modelB2(showCurrentStatus):
    n_particles, times = 100, 300
    initial_sick_percent, initial_immobilized_percent = 5, 0
    can_heal, restric_movement, infectedCantMove = True, True, True
    initial_State_A1 = createInitialState(n_particles, initial_sick_percent, initial_immobilized_percent)
    simulate(times, initial_State_A1, can_heal, restric_movement, showCurrentStatus, infectedCantMove)

def main():
#    modelA1(False)
#    modelB1(False)
     modelA2(True)
#    modelB2(False)
#    modelA3(False)
#    modelB3(False)


       
def createInitialState(n_particles, initialSick, intialCantMove):
    state = []
    nSick = (n_particles*initialSick)/100
    pDontMove = (intialCantMove)/100
    for i in range(0, n_particles):
        state.append(
            Particle(np.random.randint(bottom_movement_limit,top_movement_limit),
                     np.random.randint(bottom_movement_limit, top_movement_limit),
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
    if(p.is_infected):
        return p.x
def getYSick(p):
    if(p.is_infected):
        return p.y
def getXNotSick(p):
    if(not p.is_infected):
        return p.x
def getYNotSick(p):
    if(not p.is_infected):
        return p.y


if __name__ == "__main__":
    main()






