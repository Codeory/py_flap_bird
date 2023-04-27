"""
    玩家 小鸟
"""


class Bird:
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.flap_speed = -8
        self.down_speed = 0
        self.down_speed_acc = 1
        self.max_down_speed = 10
        self.score = 0

    def flap(self, is_flap):
        if is_flap:
            self.down_speed = self.flap_speed
            return self.down_speed
        else:
            self.down_speed += self.down_speed_acc
            return min(self.down_speed, self.max_down_speed)

    def inc_score(self, inc):
        self.score += inc

    def up_position_y(self, ground_height, bird_height, var_height):
        self.position_y = self.position_y + min(var_height,
                                                ground_height - bird_height - self.position_y)

    def get_position_y(self):
        return self.position_y

    def get_position_x(self):
        return self.position_x

    def get_score(self):
        return self.score
