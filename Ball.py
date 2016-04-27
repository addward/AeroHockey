import pygame
import Player
import math

class Ball:
    def __init__(self, Vx = 0, Vy = 0, x = 300, y = 300, a = 5, r = 12, color = (225,225,225)):
        self.Vx, self.Vy, self.x, self.y, self.a, self.r, self.color = Vx, Vy, x, y , a, r, color
        self.weight = 10

    def render(self,game):
        pygame.draw.circle(game.screen,self.color,(int(self.x),int(self.y)),self.r)

    def update(self,game):
        self.x += self.Vx * game.delta
        self.y += self.Vy * game.delta

    def speed_cal(self,player,cosa,sina):
        speedx = (self.Vx-player.vx)*sina - (self.Vy-player.vy)*cosa
        speedy = (self.Vx-player.vx)*cosa + (self.Vy-player.vy)*sina
        sqrtD = math.sqrt(4*player.weight**2*speedy**2+4*(player.weight+self.weight)*player.weight*speedx**2)
        speedy1 = (2*self.weight*speedy+sqrtD)/(2*(self.weight+player.weight))
        speedx1 = speedx
        sx1 = speedx1*sina + speedy1*cosa + player.vx
        sy1 = speedy1*sina - speedx1*cosa + player.vy
        speed = (sx1,sy1)
        return speed

    def check_hit(self, player, game):
        color = [(230,51,51),(54,116,225)]
        """Удар с правой гранью экрана"""
        if self.x + self.r + game.ethik>game.width:
            self.x = game.width - game.ethik - self.r
            self.Vx =-self.Vx

        """Удар с левой гранью экрана"""
        if self.x - self.r - game.ethik<0:
            self.x = self.r + game.ethik
            self.Vx = -self.Vx

        """Удар с нижней гранью экрана"""
        if self.y + self.r + game.ethik>game.height:
            if (self.x<game.width/2+game.gate and self.x>game.width/2-game.gate):
                game.player2.score+=1
                game.player.start_pos(game)
                game.player2.start_pos(game)
                self.start_pos(game)
            else:
                self.y = game.height - self.r - game.ethik
                self.Vy = -self.Vy

        """Удар с верхней гранью экрана"""
        if self.y-self.r - game.ethik<0:
            if (self.x<game.width/2+game.gate and self.x>game.width/2-game.gate):
                game.player.score+=1
                game.player.start_pos(game)
                game.player2.start_pos(game)
                self.start_pos(game)
            else:
                self.y = self.r + game.ethik
                self.Vy = -self.Vy

        """Удар с шаром игрока"""
        if ((self.x - player.x)**2+(self.y - player.y)**2<(self.r+player.r)**2):
            mod = math.sqrt((self.x - player.x)**2+(self.y - player.y)**2)       #Содуль вектора, соединящего центры шаров
            cosa = (self.x-player.x)/mod                                         #Косинус угла наклона вектора, соединяющего центры шаров
            sina = (self.y-player.y)/mod
            self.x = player.x + (self.r+player.r)*(self.x-player.x)/mod
            self.y = player.y + (self.r+player.r)*(self.y-player.y)/mod
            self.color = color[player._team]
            speed = self.speed_cal(player,cosa,sina)
            self.Vy = speed[1]
            self.Vx = speed[0]

    def start_pos(self,game):
        self.Vx=0
        self.Vy=0
        self.x = game.width/2
        self.y = game.height/2
        self.color = (255,255,255)
