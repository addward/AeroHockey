import pygame
import Player
import math
import Vector

class Ball:
    def __init__(self, Vx = 0, Vy = 0, x = 300, y = 300, a = 5, r = 12, color = (225,225,225)):
        self.a, self.r, self.color =a, r, color
        self.weight = 10
        self.speed = Vector.Vector([Vx,Vy])
        self.pos = Vector.Vector([x,y])

    def render(self,game):
        pygame.draw.circle(game.screen,self.color,(int(self.pos.koord[0]),int(self.pos.koord[1])),self.r)

    def update(self,game):
        self.pos +=self.speed * game.delta

    def speed_cal(self,player,cosa,sina):
        speedx = (self.speed.koord[0]-player.speed.koord[0])*sina - (self.speed.koord[1]-player.speed.koord[1])*cosa
        speedy = (self.speed.koord[0]-player.speed.koord[0])*cosa + (self.speed.koord[1]-player.speed.koord[1])*sina
        sqrtD = math.sqrt(4*player.weight**2*speedy**2+4*(player.weight+self.weight)*player.weight*speedx**2)
        speedy1 = (2*self.weight*speedy+sqrtD)/(2*(self.weight+player.weight))
        speedx1 = speedx
        sx1 = speedx1*sina + speedy1*cosa + player.speed.koord[0]
        sy1 = speedy1*sina - speedx1*cosa + player.speed.koord[1]
        return Vector.Vector([sx1,sy1])

    def check_hit(self, player, game):
        color = [(230,51,51),(54,116,225)]
        """Удар с правой гранью экрана"""
        if self.pos.koord[0] + self.r + game.ethik>game.width:
            self.pos.koord[0] = game.width - game.ethik - self.r
            self.speed.koord[0] =-self.speed.koord[0]

        """Удар с левой гранью экрана"""
        if self.pos.koord[0] - self.r - game.ethik<0:
            self.pos.koord[0] = self.r + game.ethik
            self.speed.koord[0] = -self.speed.koord[0]

        """Удар с нижней гранью экрана"""
        if self.pos.koord[1] + self.r + game.ethik>game.height:
            if (self.pos.koord[0]<game.width/2+game.gate and self.pos.koord[0]>game.width/2-game.gate):
                game.player2.score+=1
                game.player.start_pos(game)
                game.player2.start_pos(game)
                self.start_pos(game)
            else:
                self.pos.koord[1] = game.height - self.r - game.ethik
                self.speed.koord[1] = -self.speed.koord[1]

        """Удар с верхней гранью экрана"""
        if self.pos.koord[1]-self.r - game.ethik<0:
            if (self.pos.koord[0]<game.width/2+game.gate and self.pos.koord[0]>game.width/2-game.gate):
                game.player.score+=1
                game.player.start_pos(game)
                game.player2.start_pos(game)
                self.start_pos(game)
            else:
                self.pos.koord[1] = self.r + game.ethik
                self.speed.koord[1] = -self.speed.koord[1]

        """Удар с шаром игрока"""
        if ((self.pos-player.pos).mod()<math.sqrt((self.r+player.r)**2)):
            mod = (self.pos-player.pos).mod()                                       #Содуль вектора, соединящего центры шаров
            cosa = (self.pos.koord[0]-player.pos.koord[0])/mod                                         #Косинус угла наклона вектора, соединяющего центры шаров
            sina = (self.pos.koord[1]-player.pos.koord[1])/mod
            self.pos = player.pos + (self.pos-player.pos) * ((self.r+player.r) / mod)
            self.color = color[player._team]
            self.speed = self.speed_cal(player,cosa,sina)

    def start_pos(self,game):
        self.speed.koord = [0,0]
        self.pos.koord = [game.width/2,game.height/2]
        self.color = (255,255,255)
