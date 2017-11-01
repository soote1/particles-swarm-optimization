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
                random_value = self.get_random_value(-1, 1)
                self.particles[i].set_speed_in_dimension(random_value)

    def set_maximum_speed(self):
        self.maximumSpeed = 10*self.maxSpeedPercentage

    "#pending"
    def get_nearest_neighbors(self, p):
        min_neighbors = []

        for n_index in range(0, self.neighborhood):

            if p < len(self.particles) - 1:
                min_neighbor = self.particles[p + 1].get_current_position()
                min_distance = VectorArithmetic.get_euclidean_distance(
                    self.particles[p].get_current_position(),
                    min_neighbor)
                min_neighbor_index = p + 1
            else:
                min_neighbor = self.particles[p - 1].get_current_position()
                min_distance = VectorArithmetic.get_euclidean_distance(
                    self.particles[p].get_current_position(),
                    min_neighbor)
                min_neighbor_index = p - 1

            for p_index in range(0, len(self.particles)):

                current_distance = VectorArithmetic.get_euclidean_distance(
                    self.particles[p].get_current_position(),
                    self.particles[p_index].get_current_position())

                if current_distance < min_distance and p != p_index:
                    if p_index not in min_neighbors:
                        min_neighbor_index = p_index
                        min_distance = current_distance

            min_neighbors.append(min_neighbor_index)

        return min_neighbors

    def get_nearest_neighbor(self, neighbors):
        neighbor = 0
        min_fitness = VectorArithmetic.sphere_function(self.particles[neighbors[0]].get_current_position())

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
    def get_new_speed_with_neighbor(new_speed, bi, xi, hi, phi_one, phi_two):

        current_best_distance = VectorArithmetic.subtraction(bi, xi)
        current_neighbor_distance = VectorArithmetic.subtraction(hi, xi)

        '#apply influence to distances'
        current_best_influenced = VectorArithmetic.vector_by_scalar(current_best_distance, phi_one)
        current_neighbor_influenced = VectorArithmetic.vector_by_scalar(current_neighbor_distance, phi_two)

        aux = VectorArithmetic.addition(current_best_influenced, current_neighbor_influenced)

        return VectorArithmetic.addition(new_speed, aux)

    @staticmethod
    def get_new_speed(new_speed, bi, xi, phi_one):
        current_best_distance = VectorArithmetic.subtraction(bi, xi)

        '#apply influence to distances'
        current_best_influenced = VectorArithmetic.vector_by_scalar(current_best_distance, phi_one)

        return VectorArithmetic.addition(new_speed, current_best_influenced)

    def get_speed_inside_limits(self, new_speed):
        for i in range(0, len(new_speed)):
            if abs(new_speed[i]) > self.maximumSpeed:
                new_speed[i] = new_speed[i]*self.maximumSpeed / abs(new_speed[i])

        return new_speed

    @staticmethod
    def get_minimum_position(v1, v2):
        current_pos_fitness = VectorArithmetic.sphere_function(v1)
        best_pos_fitness = VectorArithmetic.sphere_function(v2)

        if current_pos_fitness < best_pos_fitness:
            return v1

        return v2

    @staticmethod
    def get_position_inside_limits(p):
        for p_index in range(0, len(p)):
            if p[p_index] > 5:
                p[p_index] = 5
            elif p[p_index] < -5:
                p[p_index] = -5

        return p

    def print_results(self, g_index):
        results_str = "Generation #" + str(g_index) + "\n"
        for p in range(0, len(self.particles)):
            results_str += "Particle #" + str(p) + "\n"
            for dim in range(0, len(self.particles[p].get_current_position())):
                results_str += str(self.particles[p].get_current_position()[dim]) + ","

            results_str += "\n"
            results_str += "Fitness: " + str(VectorArithmetic.sphere_function(
                self.particles[p].get_current_position())) + "\n"

        print(results_str)

    def main_process(self):
        for g_index in range(0, self.generations):
            for p_index in range(0, len(self.particles)):
                best_position = self.particles[p_index].get_best_position()
                current_position = self.particles[p_index].get_current_position()

                current_position_influence = self.get_random_value(0, self.phiOneMax)
                new_speed = self.particles[p_index].get_speed()

                if self.neighborhood > 0:
                    nearest_neighbors = self.get_nearest_neighbors(p_index)
                    nearest_neighbor = self.get_nearest_neighbor(nearest_neighbors)
                    neighbor_current_position = nearest_neighbor.get_current_position()
                    neighbor_position_influence = self.get_random_value(0, self.phiTwoMax)

                    new_speed = self.get_new_speed_with_neighbor(
                        new_speed,
                        best_position,
                        current_position,
                        neighbor_current_position,
                        current_position_influence,
                        neighbor_position_influence)
                else:
                    new_speed = self.get_new_speed(
                        new_speed,
                        best_position,
                        current_position,
                        current_position_influence)

                new_speed = self.get_speed_inside_limits(new_speed)
                '#check if new_position es inside limits, if not, replace with given method'
                new_position = VectorArithmetic.addition(current_position, new_speed)
                new_position = self.get_position_inside_limits(new_position)
                best_position = self.get_minimum_position(new_position, best_position)

                self.particles[p_index].set_current_position(new_position)
                self.particles[p_index].set_best_position(best_position)

            if g_index == 0 or g_index == 99:
                self.print_results(g_index)


