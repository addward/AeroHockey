import pygame
import Player
import Ball
import Start_Menu
import Server
import Mulgame


class Game:
    def tick(self):
        """Return time in seconds since previous call
        and limit speed of the game to 50 fps"""
        self.delta = self.clock.tick(70) / 1000.0

    def __init__(self,mode):
        """Constructor of the Game"""
        self._running = True
        self.size = self.width, self.height = 450, 600
        # create main display - 640x400 window
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size)#, pygame.HWSURFACE
        pygame.display.set_caption('AirHockey')
        self.clock = pygame.time.Clock()
        # set default tool
        self.tool = 'run'
        self.player  = Player.Player(1,r = 30 )   # Синий нижний игрок
        self.player.start_pos(self)
        self.player0 = Player.Player(0,r = 30 )    # Красный верхний игрок
        self.player0.start_pos(self)
        self.ball    = Ball.Ball(x = self.width/2, y = self.height/2)
        self.ethik   = 10                                                  # Толщина отступов
        self.ecolor = (255,179,0)
        self.font = pygame.font.Font('materials/9013.ttf', 100)
        self.gate = 40                                                     # Полудлина ворот
        self.mode = mode                                                   #0 - игра на одном ПК #1 - по сети

    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        elif event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                self.exit()

    def move(self):
        """Here game objects update their positions"""
        self.tick()
        self.pressed = pygame.key.get_pressed()
        self.ball.check_hit(self.player,self)
        self.ball.check_hit(self.player0,self)
        self.ball.update(self)
        self.player.update(self)
        self.player0.update(self)

    def render(self):
        """Render the scene"""
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(game.screen,self.ecolor,(0,0,self.width/2-self.gate,self.ethik))                                #Край верхней грани
        pygame.draw.rect(game.screen,self.ecolor,(self.width/2+self.gate,0,self.width,self.ethik))                       ###################
        pygame.draw.rect(game.screen,self.ecolor,(0,0,self.ethik,self.height))                                           # Край левой грани
        pygame.draw.rect(game.screen,self.ecolor,(self.width-self.ethik,0,self.ethik,self.height))                       # Край правой грани
        pygame.draw.rect(game.screen,self.ecolor,(0,self.height-self.ethik,self.width/2-self.gate,self.height))          # Край нижней грани
        pygame.draw.rect(game.screen,self.ecolor,(self.width/2+self.gate,self.height-self.ethik,self.width,self.height)) ###################
        self.player.render(self)
        self.player0.render(self)
        self.ball.render(self)
        pygame.display.flip()

    def exit(self):
        """Exit the game"""
        self._running = False

    def cleanup(self):
        """Cleanup the Game"""
        pygame.quit()

    def execute(self):
        """Execution loop of the game"""
        while(self._running):
            # get all pygame events from queue
            for event in pygame.event.get():
                self.event_handler(event)
            self.move()
            self.render()
        self.cleanup()
if __name__ == "__main__":
    s = Start_Menu.Start_Menu()
    s.execute()
    if (s.Mode==1):
        game = Game(mode=0)
        game.execute()
    if (s.Mode==3):
        server = Server.Game()
        server.execute()
    if (s.Mode==2):
        mulgame = Mulgame.Game()
        mulgame.execute()