import pygame
import Player
import math
import Vector

class Ball:
    def __init__(self,maxspeed = 300, Vx = 0, Vy = 0, x = 300, y = 300, a = 5, r = 12, color = (225,225,225)):
        self.a, self.r, self.color =a, r, color
        self.weight = 10
        self.speed = Vector.Vector(Vx,Vy)
        self.pos = Vector.Vector(x,y)
        self.maxspeed = maxspeed

    def render(self,game):
        position = (int(self.pos.x),int(self.pos.y))
        pygame.draw.circle(game.screen,self.color,position,self.r)

    def update(self,game):
        self.pos +=self.speed * game.delta

    def speed_cal(self,player,cosa,sina):
        speedx = (self.speed.x-player.speed.x)*sina - (self.speed.y-player.speed.y)*cosa
        speedy = (self.speed.x-player.speed.x)*cosa + (self.speed.y-player.speed.y)*sina
        sqrtD = math.sqrt(4*player.weight**2*speedy**2+4*(player.weight+self.weight)*player.weight*speedx**2)
        speedy1 = (2*self.weight*speedy+sqrtD)/(2*(self.weight+player.weight))
        speedx1 = speedx
        sx1 = speedx1*sina + speedy1*cosa + player.speed.x
        sy1 = speedy1*sina - speedx1*cosa + player.speed.y
        mod = math.sqrt(sx1**2+sy1**2)
        if (mod>self.maxspeed):
            sx1 = sx1*self.maxspeed/mod
            sy1 = sy1*self.maxspeed/mod
        return Vector.Vector(sx1,sy1)

    def check_hit(self, player, game):
        color = [(230,51,51),(54,116,225)]
        """Удар с правой гранью экрана"""
        if self.pos.x + self.r + game.ethik>game.width:
            self.pos.x = game.width - game.ethik - self.r
            self.speed.x =-self.speed.x

        """Удар с левой гранью экрана"""
        if self.pos.x - self.r - game.ethik<0:
            self.pos.x = self.r + game.ethik
            self.speed.x = -self.speed.x

        """Удар с нижней гранью экрана"""
        if self.pos.y + self.r + game.ethik>game.height:
            if (self.pos.x<game.width/2+game.gate and self.pos.x>game.width/2-game.gate):
                game.player0.score+=1
                game.player.start_pos(game)
                game.player0.start_pos(game)
                self.start_pos(game)
                if (game.mode == 1):
                    game.sound1.play(loops = 0)
            else:
                self.pos.y = game.height - self.r - game.ethik
                self.speed.y = -self.speed.y

        """Удар с верхней гранью экрана"""
        if self.pos.y-self.r - game.ethik<0:
            if (self.pos.x<game.width/2+game.gate and self.pos.x>game.width/2-game.gate):
                game.player.score+=1
                game.player.start_pos(game)
                game.player0.start_pos(game)
                self.start_pos(game)
                if (game.mode == 1):
                    game.sound1.play(loops = 0)
            else:
                self.pos.y = self.r + game.ethik
                self.speed.y = -self.speed.y

        """Удар с шаром игрока"""
        if ((self.pos-player.pos).mod()<math.sqrt((self.r+player.r)**2)):
            mod = (self.pos-player.pos).mod()                                       #Содуль вектора, соединящего центры шаров
            cosa = (self.pos.x-player.pos.x)/mod                                         #Косинус угла наклона вектора, соединяющего центры шаров
            sina = (self.pos.y-player.pos.y)/mod
            self.pos = player.pos + (self.pos-player.pos) * ((self.r+player.r) / mod)
            self.color = color[player._team]
            self.speed = self.speed_cal(player,cosa,sina)
            if (game.mode == 1):
                game.sound.play(loops = 0)

    def start_pos(self,game):
        self.speed = Vector.Vector(0,0)
        self.pos = Vector.Vector(game.width/2,game.height/2)
        self.color = (255,255,255)
