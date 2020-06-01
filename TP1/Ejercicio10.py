import numpy as np
import random
import matplotlib.pyplot as plt
from enum import Enum

class Board:
    def __init__(
        self,
        contagion_probability,
        heal_probability,
        heal_steps,
        top_movement_limit,
        transmission_distance,
        steps_until_not_move,
        n_particles, 
        times, 
        initial_sick_percent,
        initial_immobilized_percent,
        can_heal,
        restric_movement,
        infected_cant_move
    ):
        self.bottom_movement_limit = 0
        self.contagion_probability = contagion_probability
        self.heal_probability = heal_probability
        self.heal_steps = heal_steps
        self.top_movement_limit = top_movement_limit
        self.transmission_distance = transmission_distance
        self.steps_until_not_move = steps_until_not_move
        self.n_particles = n_particles 
        self.times = times 
        self.can_heal = can_heal
        self.restric_movement = restric_movement
        self.infected_cant_move = infected_cant_move
        self.n_infected_on_step = []
        self.n_not_infected_on_step = []
        self.state = []
        self.createInitialState(initial_sick_percent, initial_immobilized_percent)

    def createInitialState(self, initial_sick_percent, initial_immobilized_percent):
        nSick = (self.n_particles*initial_sick_percent)/100
        pDontMove = (initial_immobilized_percent)/100
        for i in range(0, self.n_particles):
            x = np.random.randint(self.bottom_movement_limit, self.top_movement_limit)
            y = np.random.randint(self.bottom_movement_limit, self.top_movement_limit)
            self.state.append(
                Particle(x,y, i < nSick, np.random.uniform(0,1) > pDontMove, self))

    def get_near_infected(self, particle):
        nearParticles = 0
        for current_particle in self.state:
            if (current_particle.is_infected and particle.is_near(current_particle)):
                nearParticles += 1
        return nearParticles
    
    def get_state_information(self):
        nInfected = (sum(p.is_infected for p in self.state))
        self.n_infected_on_step.append(nInfected)
        self.n_not_infected_on_step.append((len(self.state)-nInfected))

    def simulate(self, show_current_status = False, show_interval = 1):
        for i in range(1, self.times):
            for j in range(0, self.n_particles):
                near_infected = self.get_near_infected(self.state[j])
                self.state[j].move_particle(near_infected)
            self.get_state_information()
            if(show_current_status and ((i % show_interval) == 0)):
                self.plotCurrentStatus(i)
        self.plotFinalStatus()

    def plotCurrentStatus(self, currentTime):
        plt.cla()
        plt.xlim(self.bottom_movement_limit - 5, self.n_particles + 5)
        plt.ylim(self.bottom_movement_limit - 5, self.n_particles + 5)
        plt.scatter(list(map(self.getXSick, self.state)), list(map(self.getYSick, self.state)), color='green', label='times:  %.1f' %(currentTime), marker='^')
        plt.scatter(list(map(self.getXNotSick, self.state)), list(map(self.getYNotSick, self.state)), color='Blue')
        plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, loc='upper center')
        plt.pause(0.001)

    def getXSick(self, p):
        if(p.is_infected):
            return p.x
    def getYSick(self, p):
        if(p.is_infected):
            return p.y
    def getXNotSick(self, p):
        if(not p.is_infected):
            return p.x
    def getYNotSick(self, p):
        if(not p.is_infected):
            return p.y

    def plotFinalStatus(self):
        plt.close()
        plt.xlim(self.bottom_movement_limit - 5, self.times + 5)
        plt.ylim(self.bottom_movement_limit - 5, self.n_particles + 5)
        x_axis = list(range(self.bottom_movement_limit, self.times-1))
        plt.plot( x_axis,
                  self.n_infected_on_step,
                  color='green',
                  label='Infectados')
        plt.plot( x_axis,
                  self.n_not_infected_on_step,
                  color='blue',
                  label='Sanos')
        plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
        plt.show()

class Particle:
    def __init__(self, x, y, is_infected, can_move, board, infected_steps=0):
        self.x = x
        self.y = y
        self.is_infected = is_infected
        self.can_move = can_move
        self.board = board
        self.infected_steps = infected_steps

    def is_near(self, other_particle): 
        return ((abs(other_particle.x - self.x) <= self.board.transmission_distance) and 
                (abs(other_particle.y - self.y) <= self.board.transmission_distance))

    def move(self):
        p = np.random.uniform(0, 1)
        if   (        p < 0.25 and self.x + 1 < self.board.top_movement_limit):    self.x += 1
        elif (0.25 <= p < 0.5  and self.y + 1 < self.board.top_movement_limit):    self.y += 1
        elif (0.5  <= p < 0.75 and self.x - 1 > self.board.bottom_movement_limit): self.x -= 1
        elif (0.75 <= p        and self.y - 1 > self.board.bottom_movement_limit): self.y -= 1

    def try_heal(self):
        if(self.is_infected and self.infected_steps > self.board.heal_steps and np.random.uniform(0,1) <= self.board.heal_probability):
            self.is_infected = False
            self.can_move = True
            self.infected_steps = 0

    def is_got_infected(self, n_near_infected):
        is_infected = False
        for i in range(0, n_near_infected):
            if (self.board.contagion_probability >= np.random.uniform(0,1)):
                is_infected = True
        return is_infected

    def move_particle(self, n_near_infected):
        if(not self.board.restric_movement or self.board.restric_movement and self.can_move):
            self.move()
        if(not self.is_infected and n_near_infected > 0):
            self.is_infected = self.is_got_infected(n_near_infected)
        if(self.board.can_heal):
            self.try_heal()
        if(self.board.infected_cant_move and self.is_infected and self.infected_steps >= self.board.steps_until_not_move):
            self.can_move = False
        if (self.is_infected): self.infected_steps += 1

def main():
    n_particles = 100
    times = 4000
    initial_sick_percent = 5
    contagion_probability = 0.6
    heal_probability = 0.8
    heal_steps = 20
    top_movement_limit = 100
    transmission_distance = 2
    steps_until_not_move = 10

    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0, False, False, False
    model_A1_board = Board(
        contagion_probability,
        heal_probability,
        heal_steps,
        top_movement_limit,
        transmission_distance,
        steps_until_not_move,
        n_particles, 
        times, 
        initial_sick_percent,
        initial_immobilized_percent,
        can_heal,
        restric_movement,
        infected_cant_move
    )
    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0, True, False, False
    model_B1_board = Board(
        contagion_probability,
        heal_probability,
        heal_steps,
        top_movement_limit,
        transmission_distance,
        steps_until_not_move,
        n_particles,
        times,
        initial_sick_percent,
        initial_immobilized_percent,
        can_heal,
        restric_movement,
        infected_cant_move
    )
    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0, False, True, True
    model_A2_board = Board(
        contagion_probability,
        heal_probability,
        heal_steps,
        top_movement_limit,
        transmission_distance,
        steps_until_not_move,
        n_particles,
        times,
        initial_sick_percent,
        initial_immobilized_percent,
        can_heal,
        restric_movement,
        infected_cant_move
    )
    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0, True, True, True
    model_B2_board = Board(
        contagion_probability,
        heal_probability,
        heal_steps,
        top_movement_limit,
        transmission_distance,
        steps_until_not_move,
        n_particles,
        times,
        initial_sick_percent,
        initial_immobilized_percent,
        can_heal,
        restric_movement,
        infected_cant_move
    )
    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 50, False, True, False
    model_A3_board = Board(
        contagion_probability,
        heal_probability,
        heal_steps,
        top_movement_limit,
        transmission_distance,
        steps_until_not_move,
        n_particles,
        times,
        initial_sick_percent,
        initial_immobilized_percent,
        can_heal,
        restric_movement,
        infected_cant_move
    )
    initial_immobilized_percent, can_heal, restric_movement, infected_cant_move = 0, True, True, False
    model_B3_board = Board(
        contagion_probability,
        heal_probability,
        heal_steps,
        top_movement_limit,
        transmission_distance,
        steps_until_not_move,
        n_particles,
        times,
        initial_sick_percent,
        initial_immobilized_percent,
        can_heal,
        restric_movement,
        infected_cant_move
    )


    #Todos las particulas se mueven
        # Modelo A
    model_A1_board.simulate()
        # Modelo B
    model_B1_board.simulate()
    #10 Instantes luego de que la particula se infecte, deja de moverse
        #Modelo A
    model_A2_board.simulate()
        #Modelo B
    model_B2_board.simulate()
    #50 % de las particulas no se mueven
        #Modelo A
    model_A3_board.simulate()
        #Modelo B
    model_B3_board.simulate()




if __name__ == "__main__":
    main()






