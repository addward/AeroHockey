import pygame
import Player
import Ball
import socket


class Game:
    def tick(self):
        """Return time in seconds since previous call
        and limit speed of the game to 50 fps"""
        self.delta = self.clock.tick(30) / 1000.0

    def __init__(self):
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
        self.players = (self.player0,self.player)
        self.ball    = Ball.Ball(x = self.width/2, y = self.height/2)
        self.ethik   = 10                                                  # Толщина отступов
        self.ecolor = (255,179,0)
        self.font = pygame.font.Font('materials/9013.ttf', 100)
        self.gate = 40                                                     # Полудлина ворот
        self.number = 0
        self.connect_server()
        self.mode = 2
        pygame.mouse.set_visible(False)

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
        #self.pressed = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        self.sock.send(str((pos[0],pos[1])).encode())
        pos = self.sock.recv(1024)
        score = self.player.score+self.player0.score
        self.decode_pos(pos)
        if (score != self.player.score+self.player0.score):
            pygame.mouse.set_pos(self.players[self.number].pos.x,self.players[self.number].pos.y)

    def render(self):
        """Render the scene"""
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen,self.ecolor,(0,0,self.width/2-self.gate,self.ethik))                                #Край верхней грани
        pygame.draw.rect(self.screen,self.ecolor,(self.width/2+self.gate,0,self.width,self.ethik))                       ###################
        pygame.draw.rect(self.screen,self.ecolor,(0,0,self.ethik,self.height))                                           # Край левой грани
        pygame.draw.rect(self.screen,self.ecolor,(self.width-self.ethik,0,self.ethik,self.height))                       # Край правой грани
        pygame.draw.rect(self.screen,self.ecolor,(0,self.height-self.ethik,self.width/2-self.gate,self.height))          # Край нижней грани
        pygame.draw.rect(self.screen,self.ecolor,(self.width/2+self.gate,self.height-self.ethik,self.width,self.height)) ###################
        self.player.render(self)
        self.player0.render(self)
        self.ball.render(self)
        pygame.display.flip()
        #self.i+=1
        #while (self.i==30):
            #print("1: " + str(self.player.pos.x) + " " + str(self.player.pos.y))
            #self.i=0

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

    def connect_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file = open("Multiplayer_settings.txt","r")
        buff = file.read()
        file.close()
        flag = 0
        "Read the ip from txt"
        for i in range(len(buff)):
            if (flag==0 and buff[i]==":"):
                start = i+1
                flag += 1
            if (flag==1 and buff[i]=="\n"):
                end = i
                flag +=1
        self.ip = buff[start:end]
        "Read the Port"
        for i in range(end,len(buff)):
            if (flag==2 and buff[i]==":"):
                start = i+1
                flag += 1
            if (flag==3 and buff[i]=="\n"):
                end = i
                flag +=1
        self.port = buff[start:end]
        self.sock.connect((self.ip,int(self.port)))
        print('hio')
        number = self.sock.recv(1024)
        self.number = int(number.decode())

        self.sock.settimeout(10)

    def decode_pos(self, position):
        pos = position.decode()
        flag = 0
        start = 1
        end = 0
        for i in range(len(pos)):
            if (flag == 0 and pos[i] == ','):
                end = i
                self.player0.pos.x = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1

            if (flag == 1 and pos[i] == ','):
                end = i
                self.player0.pos.y = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1

            if (flag == 2 and pos[i] == ','):
                end = i
                self.player.pos.x = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1

            if (flag == 3 and pos[i] == ','):
                end = i
                self.player.pos.y = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1


            if (flag == 4 and pos[i] == ','):
                end = i
                self.ball.pos.x = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1

            if (flag == 5 and pos[i] == ','):
                end = i
                self.ball.pos.y = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1

            if (flag == 6 and pos[i] == ','):
                end = i
                self.player0.score = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1

            if (flag == 7 and pos[i] == ')'):
                end = i
                self.player.score = int(float(pos[start:end]))
                break