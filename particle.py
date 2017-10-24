class Particle:

    def __init__(self):
        self.currentPosition = []
        self.speed = []
        self.bestPosition = []

    def get_current_position(self):
        return self.currentPosition

    def set_current_position(self, position):
        self.currentPosition = position

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_best_position(self):
        return self.bestPosition

    def set_best_position(self, best_position):
        self.bestPosition = best_position

    def set_position_in_dimension(self, p):
        self.currentPosition.append(p)

    def set_best_position_in_dimension(self, p):
        self.bestPosition.append(p)

    def set_speed_in_dimension(self, s):
        self.speed.append(s)
