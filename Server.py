import pygame
import Player
import Ball
import socket
import Cursor


class Game:
    def tick(self):
        """Return time in seconds since previous call
        and limit speed of the game to 50 fps"""
        self.delta = self.clock.tick(70) / 1000.0

    def __init__(self):
        """Constructor of the Game"""
        self._running = True
        self.size = self.width, self.height = 450, 600
        # create main display - 640x400 window
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode((400,200))#, pygame.HWSURFACE
        pygame.display.set_caption('AirHockey Server')
        self.clock = pygame.time.Clock()
        # set default tool
        self.tool = 'run'
        self.player  = Player.Player(1,r = 30 )   # Синий нижний игрок
        self.player.start_pos(self)
        self.cursor1 = Cursor.Cursor(player=self.player,game=self)
        self.player0 = Player.Player(0,r = 30 )    # Красный верхний игрок
        self.player0.start_pos(self)
        self.cursor0 = Cursor.Cursor(player=self.player0,game=self)
        self.players = (self.player0, self.player)
        self.ball    = Ball.Ball(x = self.width/2, y = self.height/2)
        self.ethik   = 10                                                  # Толщина отступов
        self.ecolor = (255,179,0)
        self.gate = 40                                                     # Полудлина ворот
        self.pressed = pygame.key.get_pressed()
        self.cursor_text = 5
        self.start_server()
        self.cursors = (self.cursor0,self.cursor1)
        self.mode = 3

    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()

    def move(self):
        """Here game objects update their positions"""
        self.tick()
        #self.pressed = pygame.key.get_pressed()
        self.recieve(0)
        self.recieve(1)
        self.ball.check_hit(self.player,self)
        self.ball.check_hit(self.player0,self)
        self.ball.update(self)
        self.player.update(self)
        self.player0.update(self)
        self.send(0)
        self.send(1)

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
        self.cleanup()

    def start_server(self):
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
        self.sock.bind((self.ip,int(self.port)))

        self.print('Server has been created '+ str(self.ip)+":"+str(self.port))
        self.print("Waiting for players...100s")

        self.sock.settimeout(50)
        self.sock.listen(2)

        self.pladr1 = self.sock.accept()

        self.print("player "+str(self.pladr1[1])+"connected")

        self.pladr2 = self.sock.accept()

        self.print("player "+str(self.pladr1[1])+"connected")

        self.pladress = (self.pladr1[0],self.pladr2[0])

        self.pladress[0].send(str(0).encode())
        self.pladress[1].send(str(1).encode())

        self.pladress[0].settimeout(10)
        self.pladress[1].settimeout(10)

    def print(self, text, type = 'add'):
        self.font1 = pygame.font.Font(None, 20)
        Object = self.font1.render(text, True,(255,255,255))
        if (self.cursor_text<600 and type == 'add'):
            self.screen.blit(Object,(5,self.cursor_text))
            self.cursor_text += 20
        elif (type == 'add'):
            self.screen.fill((0,0,0))
            self.screen.blit(Object,(5,0))
            self.cursor_text = 20
        elif (type == 'new'):
            self.screen.fill((0,0,0))
            self.screen.blit(Object,(5,0))
        pygame.display.flip()

    def recieve(self,number):
        recv = self.pladress[number].recv(1024)
        self.decode_pos(recv,number)

    def send(self,number):
        self.pladress[number].send(str((self.player0.pos.x,self.player0.pos.y,self.player.pos.x,self.player.pos.y,self.ball.pos.x,self.ball.pos.y,self.player0.score,self.player.score)).encode())
        '''except socket.error:
            pass'''

    def decode_pos(self, mposition, number):
        pos = mposition.decode()
        flag = 0
        start = 1
        end = 0
        for i in range(len(pos)):
            if (flag == 0 and pos[i] == ','):
                end = i
                mousex = float(pos[start:end])
                #self.player.pos.x = int(float(pos[start:end]))
                flag += 1
                start = end + 2
                i+=1

            if (flag == 1 and pos[i] == ')'):
                end = i
                mousey = float(pos[start:end])
                #self.player0.pos.y = int(float(pos[start:end]))
                break
        if (number == 0) : self.print(str(number) + " x= " + str(mousex) + " " + "y= " + str(mousey),type='new')
        self.cursors[number].move_player_to(mousex,mousey)
