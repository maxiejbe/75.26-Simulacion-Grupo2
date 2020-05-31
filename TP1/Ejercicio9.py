import numpy as np
import random
from matplotlib import pyplot as plt
from enum import Enum


class Direction(Enum):
    north = 0
    south = 1
    east = 2
    west = 3


class Board:
    def __init__(
        self, size_x, size_y, green_particles_count, red_particles_count, moving_time
    ):
        self.size_x = size_x
        self.size_y = size_y

        self.time = 0
        self.moving_time = moving_time

        self.green_particles_count = green_particles_count
        self.green_particles = []

        self.red_particles = []
        self.red_particles_count = red_particles_count

        self.initialize_particles()

    def initialize_green_particles(self):
        for i in range(1, self.green_particles_count):
            x = np.random.uniform(0, self.size_x / 2)
            y = np.random.uniform(0, self.size_y)
            self.green_particles.append(Particle(x, y))

    def initialize_red_particles(self):
        for i in range(1, self.red_particles_count):
            x = np.random.uniform(self.size_x / 2, self.size_x)
            y = np.random.uniform(0, self.size_y)
            self.red_particles.append(Particle(x, y))

    def initialize_particles(self):
        # Move maybe this logic to particle
        self.initialize_green_particles()
        self.initialize_red_particles()

    def start_movement(self):
        while self.time <= self.moving_time:
            for p in self.green_particles:
                p.move()
            for p in self.red_particles:
                p.move()
            self.time += 1
            self.draw()

    def draw(self):
        plt.cla()
        plt.xlim(0, self.size_x)
        plt.ylim(0, self.size_y)
        plt.scatter(
            list(p.get_x() for p in self.green_particles),
            list(p.get_y() for p in self.green_particles),
            color="green",
            label="times:  %.1f" % (self.time),
        )
        plt.scatter(
            list(p.get_x() for p in self.red_particles),
            list(p.get_y() for p in self.red_particles),
            color="black",
        )
        plt.legend(
            fancybox=True, framealpha=1, shadow=True, borderpad=1, loc="upper center"
        )
        plt.pause(0.001)


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.directions = self.generate_directions()
        self.particle_step = 0.1

    def move_to_north(self):
        self.y += self.particle_step

    def move_to_south(self):
        self.y -= self.particle_step

    def move_to_east(self):
        self.x += self.particle_step

    def move_to_west(self):
        self.x -= self.particle_step

    def generate_directions(self):
        direction_actions = []
        direction_actions.append(self.move_to_north)
        direction_actions.append(self.move_to_south)
        direction_actions.append(self.move_to_east)
        direction_actions.append(self.move_to_west)
        return direction_actions

    def move(self):
        direction = random.randrange(len(Direction))
        self.directions[direction]()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


def main():
    green_particles_count, red_particles_count = 100, 100
    board_size_x, board_size_y = 10, 20
    moving_time = 3000

    board = Board(
        board_size_x,
        board_size_y,
        green_particles_count,
        red_particles_count,
        moving_time,
    )
    board.start_movement()

    print("test")


if __name__ == "__main__":
    main()
