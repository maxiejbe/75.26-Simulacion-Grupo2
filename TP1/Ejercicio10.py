import numpy as np
import random
import matplotlib.pyplot as plt
from enum import Enum

contagionProbability = 0.6
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
    def is_near(self, other_particle):
        return (other_particle.x <= self.x + transmission_distance and 
                other_particle.x >= self.x - transmission_distance and
                other_particle.y <= self.y + transmission_distance and 
                other_particle.y >= self.y - transmission_distance)
    def move(self):
        p = np.random.uniform(0, 1)
        if   (        p < 0.25 and self.x + 1 < top_movement_limit):    self.x += 1
        elif (0.25 <= p < 0.5  and self.y + 1 < top_movement_limit):    self.y += 1
        elif (0.5  <= p < 0.75 and self.x - 1 > bottom_movement_limit): self.x -= 1
        elif (0.75 <= p        and self.y - 1 > bottom_movement_limit): self.y -= 1

    def try_heal(self):
        if(self.is_infected and self.infected_steps > heal_steps and np.random.uniform(0,1) <= heal_probability):
            self.is_infected = False
            self.can_move = True
            self.infected_steps = 0;

    def is_got_infected(self, n_near_infected):
        is_infected = True
        for i in range(1, n_near_infected):
            if (contagionProbability >= np.random.uniform(0,1)):
                is_infected = True
        return is_infected

    def move_particle(self, n_near_infected, heal, restric_movement, infected_cant_move):
        if(not restric_movement or restric_movement and self.can_move):
            self.move()
        if(not self.is_infected and n_near_infected > 0):
            self.is_infected = self.is_got_infected(n_near_infected)
        if(heal):
            self.try_heal()
        if(infected_cant_move and self.is_infected and self.infected_steps >= steps_until_not_move):
            self.can_move = False
        if (self.is_infected): self.infected_steps += 1

def get_near_infected(particle, other_particles):
    nearParticles = []
    for currentParticle in other_particles:
        if (currentParticle.is_infected and particle.is_near(currentParticle)):
            nearParticles.append(currentParticle)
    return nearParticles

def simulate(times, state, can_heal, restric_movement, infected_cant_move, show_current_status, show_interval ):
    print('times: ', times, 'can_heal: ',can_heal , 'restric_movement: ', restric_movement, 'infected_cant_move: ', infected_cant_move)
    infected, not_infected, ntimes = [], [], []
    for i in range(1, times):
        for j in range(0, len(state)):
            nearInfected = get_near_infected(state[j], state)
            state[j].move_particle(len(nearInfected), can_heal, restric_movement, infected_cant_move)
        
        nInfected = (len([particle for particle in state if particle.is_infected]))
        infected.append(nInfected)
        not_infected.append((len(state)-nInfected))
        ntimes.append(i)
        if(show_current_status and ((i % show_interval) == 0)):
            plotCurrentStatus(i, state)

    plotFinalStatus(infected, not_infected, ntimes)

def createModel(n_particles, times, initial_sick_percent, initial_immobilized_percent, can_heal, 
                restric_movement, show_current_status, show_interval, infected_cant_move):
    initial_state = createInitialState(n_particles, initial_sick_percent, initial_immobilized_percent)
    simulate(times, initial_state, can_heal, restric_movement, infected_cant_move, show_current_status, show_interval)

       
def createInitialState(n_particles, initialSick, intialCantMove):
    state = []
    nSick = (n_particles*initialSick)/100
    pDontMove = (intialCantMove)/100
    for i in range(0, n_particles):
        state.append(
            Particle(np.random.randint(bottom_movement_limit,top_movement_limit),
                     np.random.randint(bottom_movement_limit, top_movement_limit),
                     i < nSick,
                     np.random.uniform(0,1) > pDontMove))
    return state

def plotCurrentStatus(currentTime, currentState):
    plt.cla()
    plt.xlim(bottom_movement_limit, top_movement_limit)
    plt.ylim(bottom_movement_limit, top_movement_limit)
    plt.scatter(list(map(getXSick, currentState)), list(map(getYSick, currentState)), color='green', label='times:  %.1f' %(currentTime))
    plt.scatter(list(map(getXNotSick, currentState)), list(map(getYNotSick, currentState)), color='black')
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, loc='upper center')
    plt.pause(0.00001)

def plotFinalStatus(infected, not_infected, ntimes):
    plt.close()
    plt.xlim(-5, 4005)
    plt.ylim(-5, 105)
    plt.plot(ntimes, infected, color='green', label='Infectados')
    plt.plot(ntimes, not_infected, color='blue', label='Sanos')
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


def main():
    n_particles, times, initial_sick_percent = 100, 4000, 5
    show_current_status, show_interval = True, 10

#    #Todos las particulas se mueven
#        # Modelo A
#    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0, False, False, False
#    createModel(n_particles, times, initial_sick_percent, initial_immobilized_percent, can_heal, restric_movement, 
#    show_current_status, show_interval, infected_cant_move)
#        # Modelo B
#    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0 , True, False, False
#    createModel(n_particles, times, initial_sick_percent, initial_immobilized_percent, can_heal, restric_movement, 
#    show_current_status, show_interval, infected_cant_move)
#
#    #10 Instantes luego de que la particula se infecte, deja de moverse
#        #Modelo A
#    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0 , False, True, True
#    createModel(n_particles, times, initial_sick_percent, initial_immobilized_percent, can_heal, restric_movement, 
#    show_current_status, show_interval, infected_cant_move)
#        #Modelo B
#    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0 , True, True, True
#    createModel(n_particles, times, initial_sick_percent, initial_immobilized_percent, can_heal, restric_movement, 
#    show_current_status, show_interval, infected_cant_move)
#
#    #50 % de las particulas no se mueven
#        #Modelo A
#    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 50, False, True, False
#    createModel(n_particles, times, initial_sick_percent, initial_immobilized_percent, can_heal, restric_movement, 
#    show_current_status, show_interval, infected_cant_move)
#        #Modelo B
#    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 50, True, True, False
#    createModel(n_particles, times, initial_sick_percent, initial_immobilized_percent, can_heal, restric_movement, 
#    show_current_status, show_interval, infected_cant_move)



if __name__ == "__main__":
    main()





