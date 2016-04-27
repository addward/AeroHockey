import pygame

class Start_Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300,300))
        pygame.display.set_caption('AirHockey')
        self._running = True
        self.font = pygame.font.Font('materials/9013.ttf', 70)
        self.font1 = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()
        self.Mode = 0
    def execute(self):
        """Execution loop of the game"""
        while(self._running):
            # get all pygame events from queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    return (-1)
                pos = self.render()
                if (pos == 4):
                    self.Mode = 1
                    return
    def render(self):
        self.clock.tick(50)
        self.screen.fill((183, 196, 96))
        pos = self.check()
        Object = self.font.render('Air Hockey', True,(14,118,236))
        if pos == 2:
            Object1 = self.font1.render('Singleplayer Game', True,(23, 85, 139))
            Object2 = self.font1.render('Multiplayer Game', True,(14, 118, 236))
        elif pos == 1:
            Object2 = self.font1.render('Multiplayer Game', True,(23, 85, 139))
            Object1 = self.font1.render('Singleplayer Game', True,(14, 118, 236))
        else:
            Object2 = self.font1.render('Multiplayer Game', True,(14,118,236))
            Object1 = self.font1.render('Singleplayer Game', True,(14, 118, 236))
        self.screen.blit(Object,(15,30))
        self.screen.blit(Object1,(10,120))
        self.screen.blit(Object2,(10,170))
        pygame.display.flip()
        return pos
    def check(self):
        pos = pygame.mouse.get_pos()
        key = pygame.mouse.get_pressed()
        if (pos[0]>=10 and pos[0])<=255:                       #Multiplayer
            if (pos[1]>=170 and pos[1]<=200):
                if key[0] == False:
                    return 1
                else:
                    return 3
        if (pos[0]>=10 and pos[0])<=280:                         #SinglePlayer
            if (pos[1]>=120 and pos[1]<=145):
                if key[0] == False:
                    return 2
                else:
                    return 4


