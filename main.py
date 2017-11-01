from pso.psoAlgorithm import PSOAlgorithm
from pso.particle import Particle


def main():
    dimensions = 10
    generations = 100
    max_speed_percentage = 0.1
    neighborhood = 10
    particles = [Particle() for i in range(0, 20)]
    phi_one_max = 2.05
    phi_two_max = 2.05

    pso_algorithm_helper = PSOAlgorithm(
        neighborhood,
        generations,
        particles,
        phi_one_max,
        phi_two_max,
        max_speed_percentage,
        dimensions)

    pso_algorithm_helper.do_algorithm()


if __name__ == '__main__':
    main()

