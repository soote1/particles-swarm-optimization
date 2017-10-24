import math


class VectorArithmetic:

    @staticmethod
    def greater(v1, v2):

        return

    @staticmethod
    def addition(v1, v2):
        res = []

        for i in range(0, len(v1)):
            res.append(v1[i] + v2[i])

        return res

    @staticmethod
    def vector_by_scalar(v, s):
        res = []

        for i in range(0, len(v)):
            res.append(v[i] * s)

        return res

    @staticmethod
    def subtraction(v1, v2):
        res = []

        for i in range(0, len(v1)):
            res.append(v1[i] - v2[i])

        return res

    @staticmethod
    def get_euclidean_distance(v1, v2):

        addition = 0
        for v_index in range(0, len(v1)):
            addition += pow(v1[v_index] - v2[v_index], 2)

        return math.sqrt(addition)

    @staticmethod
    def get_magnitude(v):
        addition = 0
        for v_index in range(0, len(v)):
            addition += pow(v[v_index], 2)

        return math.sqrt(addition)

    @staticmethod
    def sphere_function(v):
        addition = 0
        for v_index in range(0, len(v)):
            addition += pow(v[v_index], 2)

        return addition



