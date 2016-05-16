import Vector
import Player

class Cursor:
    def __init__(self, game, player, x = 0, y = 0, speed = 10, epsilon = 10):
        self.pos = Vector.Vector(x,y)
        self.speed = speed
        self.player = player
        self.epsilon = epsilon
        self.game = game

    def move_player_to(self, x, y):
        sub = Vector.Vector(x,y)-self.player.pos
        if (sub.mod()>self.epsilon):
            try: cosa = (x - self.player.pos.x)/sub.mod()
            except ZeroDivisionError:
                cosa=0
            try: sina = (y - self.player.pos.y)/sub.mod()
            except ZeroDivisionError:
                sina=0
            self.player.pos.x += cosa*self.speed
            self.player.pos.y += sina*self.speed
            self.player.speed.x = cosa*self.speed*20
            self.player.speed.y = sina*self.speed*20
            self.pos.x = x
            self.pos.y = y
        else:
            self.player.speed.x = 0
            self.player.speed.x = 0


