from pso.vectorArithmethic import VectorArithmetic
from random import uniform


class PSOAlgorithm:

    def __init__(self, neighborhood, generations,
                 particles, phi_one_max, phi_two_max,
                 max_speed_percentage, dimensions):

        self.neighborhood = neighborhood
        self.generations = generations
        self.particles = particles
        self.phiOneMax = phi_one_max
        self.phiTwoMax = phi_two_max
        self.maxSpeedPercentage = max_speed_percentage
        self.dimensions = dimensions
        self.maximumSpeed = 0

    def do_algorithm(self):
        self.set_initial_values()
        self.main_process()

    def set_initial_population(self):
        for i in range(0, len(self.particles)):
            for j in range(0, self.dimensions):
                random_value = self.get_random_value(-5, 5)
                self.particles[i].set_position_in_dimension(random_value)
                self.particles[i].set_best_position_in_dimension(random_value)
                random_value = self.get_random_value(-5, 5)
                self.particles[i].set_speed_in_dimension(random_value)

    def set_maximum_speed(self):
        self.maximumSpeed = 10*self.maxSpeedPercentage

    "#pending"
    def get_nearest_neighbors(self, p):
        min_neighbors = []
        min_neighbor = self.particles[0].get_current_position()
        min_distance = VectorArithmetic.get_euclidean_distance(
            p.get_current_position(),
            min_neighbor.get_current_position)
        min_neighbors.append(0)

        for n_index in range(0, self.neighborhood):

            for p_index in range(0, len(self.particles)):

                current_distance = VectorArithmetic.get_euclidean_distance(
                    p.get_current_position(),
                    min_neighbor.get_current_position)

                if current_distance < min_distance:
                    if current_distance not in min_neighbors:
                        min_neighbors.append(p_index)

        return min_neighbors

    def get_nearest_neighbor(self, neighbors):
        neighbor = 0
        min_fitness = VectorArithmetic.sphere_function(neighbors[0].get_current_position())

        for n_index in range(0, len(neighbors)):

            current_fitness = VectorArithmetic.sphere_function(
                self.particles[neighbors[n_index]].get_current_position())

            if current_fitness < min_fitness:
                neighbor = neighbors[n_index]
                min_fitness = current_fitness

        return self.particles[neighbor]

    @staticmethod
    def get_random_value(from_value, to_value):

        return uniform(from_value, to_value)

    def set_initial_values(self):
        self.set_initial_population()
        self.set_maximum_speed()

    @staticmethod
    def get_new_speed(new_speed, bi, xi, hi, phi_one, phi_two):

        current_best_distance = VectorArithmetic.subtraction(bi, xi)
        current_neighbor_distance = VectorArithmetic.subtraction(hi, xi)

        '#apply influence to distances'
        current_best_influenced = VectorArithmetic.vector_by_scalar(current_best_distance, phi_one)
        current_neighbor_influenced = VectorArithmetic.vector_by_scalar(current_neighbor_distance, phi_two)

        aux = VectorArithmetic.addition(current_best_influenced, current_neighbor_influenced)

        return VectorArithmetic.addition(new_speed, aux)

    def get_speed_inside_limits(self, new_speed):
        for i in range(0, len(new_speed)):
            if new_speed[i] > self.maximumSpeed:
                new_speed[i] = new_speed*self.maximumSpeed / VectorArithmetic.get_magnitude(new_speed)

        return new_speed

    @staticmethod
    def get_minimum_position(v1, v2):
        current_pos_fitness = VectorArithmetic.sphere_function(v1)
        best_pos_fitness = VectorArithmetic.sphere_function(v2)

        if current_pos_fitness < best_pos_fitness:
            return v1

        return v2

    def main_process(self):
        for g_index in range(0, self.generations):
            for p_index in range(0, len(self.particles)):
                best_position = self.particles[p_index].get_best_position()
                current_position = self.particles[p_index].get_current_position()
                nearest_neighbors = self.get_nearest_neighbors(self.particles[p_index])
                nearest_neighbor = self.get_nearest_neighbor(nearest_neighbors)
                neighbor_current_position = nearest_neighbor.get_current_position()
                current_position_influence = self.get_random_value(0, self.phiOneMax)
                best_position_influence = self.get_random_value(0, self.phiTwoMax)

                new_speed = self.particles[p_index].get_speed()

                new_speed = self.get_new_speed(
                    new_speed,
                    best_position,
                    current_position,
                    neighbor_current_position,
                    current_position_influence,
                    best_position_influence)

                new_speed = self.get_speed_inside_limits(new_speed)
                new_position = VectorArithmetic.addition(current_position, new_speed)
                best_position = self.get_minimum_position(new_position, best_position)

                self.particles[p_index].set_current_position(new_position)
                self.particles[p_index].set_best_position(best_position)

