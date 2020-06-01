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
        self,
        size_x,
        size_y,
        green_particles_count,
        red_particles_count,
        moving_time,
        particle_step,
        use_half_wall,
    ):
        self.size_x = size_x
        self.size_y = size_y

        self.time = 0
        self.moving_time = moving_time

        self.particle_step = particle_step

        self.green_particles, self.red_particles = [], []
        self.green_particles_count = green_particles_count
        self.red_particles_count = red_particles_count

        self.use_half_wall = use_half_wall

        self.left_green_particles_count, self.right_green_particles_count = [], []
        self.left_red_particles_count, self.right_red_particles_count = [], []

        self.initialize_particles()

    def get_particle_step(self):
        return self.particle_step

    def get_size(self):
        return self.size_x, self.size_y

    def initialize_green_particles(self):
        for i in range(1, self.green_particles_count):
            x = np.random.uniform(0, self.size_x / 2)
            y = np.random.uniform(0, self.size_y)
            self.green_particles.append(Particle(x, y, self))

    def initialize_red_particles(self):
        for i in range(1, self.red_particles_count):
            x = np.random.uniform(self.size_x / 2, self.size_x)
            y = np.random.uniform(0, self.size_y)
            self.red_particles.append(Particle(x, y, self))

    def initialize_particles(self):
        # Move maybe this logic to particle
        self.initialize_green_particles()
        self.initialize_red_particles()

    def register_particles_count(self):
        self.left_green_particles_count.append(
            sum(p.is_in_left_side() for p in self.green_particles)
        )
        self.right_green_particles_count.append(
            sum(p.is_in_right_side() for p in self.green_particles)
        )

        self.left_red_particles_count.append(
            sum(p.is_in_left_side() for p in self.red_particles)
        )
        self.right_red_particles_count.append(
            sum(p.is_in_right_side() for p in self.red_particles)
        )

    def start_movement(self):
        while self.time < self.moving_time:
            for p in self.green_particles:
                p.move()
            for p in self.red_particles:
                p.move()
            self.time += 1
            self.register_particles_count()
            # if self.time % 20 == 0:
            self.draw()
        plt.show()

    def validate_boundaries(self, x, y):
        wall_crosses_y = wall_crosses_x_left = wall_crosses_x_right = False
        if self.use_half_wall:
            wall_crosses_y = y >= self.size_y / 2
            wall_crosses_x_left = x >= (self.size_x / 2 - self.particle_step)
            wall_crosses_x_right = x <= (self.size_x / 2 + self.particle_step)

        if wall_crosses_y & wall_crosses_x_left & wall_crosses_x_right:
            return False
        if x < 0:
            return False
        if x > self.size_x:
            return False
        if y < 0:
            return False
        if y > self.size_y:
            return False
        return True

    def draw_density(self, left_particles_count, right_particles_count, color):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel("Time")
        ax.set_ylabel("Particles count (right, left)")
        x = np.linspace(0, self.moving_time, self.moving_time)
        ax.plot(x, self.right_red_particles_count, color)
        ax.plot(x, self.left_red_particles_count, color)
        plt.show()

    def draw_particles_density(self):
        self.draw_density(
            self.left_red_particles_count, self.right_red_particles_count, "-r"
        )
        self.draw_density(
            self.left_green_particles_count, self.right_green_particles_count, "-g"
        )

    def draw(self):
        plt.cla()
        plt.xlim(0, self.size_x)
        plt.ylim(0, self.size_y)
        plt.scatter(
            list(p.get_x() for p in self.green_particles),
            list(p.get_y() for p in self.green_particles),
            color="green",
            label="Time:  %.1f" % (self.time),
            marker=",",
            lw=0,
            s=3,
        )
        plt.scatter(
            list(p.get_x() for p in self.red_particles),
            list(p.get_y() for p in self.red_particles),
            color="red",
            marker=",",
            lw=0,
            s=3,
        )

        if self.use_half_wall:
            wall_x = [self.size_x / 2, self.size_x / 2]
            wall_y = [self.size_y, self.size_y / 2]
            plt.plot(wall_x, wall_y, marker="o", color="black")

        plt.legend(
            fancybox=True, framealpha=1, shadow=True, borderpad=1, loc="upper center"
        )
        plt.pause(0.0001)


class Particle:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.directions = self.generate_directions()
        self.board = board
        self.particle_step = board.get_particle_step()

    def move_to_north(self):
        new_y = self.y + self.particle_step
        if self.board.validate_boundaries(self.x, new_y):
            self.y = new_y

    def move_to_south(self):
        new_y = self.y - self.particle_step
        if self.board.validate_boundaries(self.x, new_y):
            self.y = new_y

    def move_to_east(self):
        new_x = self.x + self.particle_step
        if self.board.validate_boundaries(new_x, self.y):
            self.x = new_x

    def move_to_west(self):
        new_x = self.x - self.particle_step
        if self.board.validate_boundaries(new_x, self.y):
            self.x = new_x

    def is_in_left_side(self):
        size_x, size_y = self.board.get_size()
        return self.x < size_x / 2

    def is_in_right_side(self):
        size_x, size_y = self.board.get_size()
        return self.x > size_x / 2

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
    green_particles_count, red_particles_count = 10000, 10000
    board_size_x, board_size_y = 10, 20
    particle_step = 0.1
    moving_time = 3000

    # a) En t=0 la pared divisoria es retirada, permitiendo que los dos gases se mezclen
    board = Board(
        board_size_x,
        board_size_y,
        green_particles_count,
        red_particles_count,
        moving_time,
        particle_step,
        False,
    )
    board.start_movement()
    board.draw_particles_density()

    # b) En t=0 es removida sólo la mitad inferior de la pared permitiendo que los dos gases se mezclen
    board = Board(
        board_size_x,
        board_size_y,
        green_particles_count,
        red_particles_count,
        moving_time,
        particle_step,
        True,
    )
    board.start_movement()
    board.draw_particles_density()


if __name__ == "__main__":
    main()
