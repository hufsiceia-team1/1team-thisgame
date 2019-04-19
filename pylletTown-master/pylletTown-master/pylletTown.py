import pygame
import tmx
import character
import random
from pygame.locals import *
import sys, os
from menu import *
from effect import *
import sound


R = render()
pygame.mixer.music.load('music/Pacman_Introduction_Music-KP-826387403.wav')
pygame.init()
pygame.mixer.music.play()

class name():
    def __init__(self):
        self.name_ = 's'

    def mkname(self,new_name):
        self.new_name = new_name
        return new_name

if __name__ == "__main__":
    class Game:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.clock = pygame.time.Clock()

        def draw_text(self, text, size, x, y, center=True):
            # utility function to draw text at a given location
            font_name = pygame.font.match_font('arial')
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            if center:
                text_rect.midtop = (x, y)
            else:
                text_rect.topleft = (x, y)
            return self.screen.blit(text_surface, text_rect)

    g = Game()
    font = pygame.font.match_font("Ubuntu Mono")
    # standard list of options and customized labels
    items = {"play": "Play", "opt": "How to", "quit": "Quit"}
    menu = GameMenu(g, "POKEMON", ["Play", "How to", "Quit"], font=font, font_size=40)
    menu.run()
    print("starting game")
    pygame.mixer.music.load('music/Challenge_Mode.mp3')
    pygame.init()
    pygame.mixer.music.play()





pygame.time.set_timer(pygame.USEREVENT,1000)



class SpriteLoop(pygame.sprite.Sprite):
    """A simple looped animated sprite.
    
    SpriteLoops require certain properties to be defined in the relevant
    tmx tile:
    
    src - the source of the image that contains the sprites
    width, height - the width and height of each section of the sprite that
        will be displayed on-screen during animation
    mspf - milliseconds per frame, or how many milliseconds must pass to 
        advance onto the next frame in the sprite's animation 
    frames - the number individual frames that compose the animation
    """
    def __init__(self, location, cell, *groups):
        super(SpriteLoop, self).__init__(*groups)
        self.image = pygame.image.load(cell['src'])
        self.defaultImage = self.image.copy()
        self.width = int(cell['width'])
        self.height = int(cell['height'])
        self.rect = pygame.Rect(location, (self.width,self.height))
        self.frames = int(cell['frames'])
        self.frameCount = 0
        self.mspf = int(cell['mspf']) # milliseconds per frame
        self.timeCount = 0

    def update(self, dt, game):
        self.timeCount += dt
        if self.timeCount > self.mspf:
            # Advance animation to the appropriate frame
            self.image = self.defaultImage.copy()
            self.image.scroll(-1*self.width*self.frameCount, 0)
            self.timeCount = 0
            
            self.frameCount += 1
            if self.frameCount == self.frames:
                self.frameCount = 0
        
class Game(object):         ##############게임

    def __init__(self, screen):
        self.screen = screen

    def initArea(self, mapFile):
        """Load maps and initialize sprite layers for each new area"""
        self.tilemap = tmx.load(mapFile, screen.get_size())
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()

        #self.life = pygame.image.load('life.png')
        #self.gamefont = pygame.font.Font(None,30)
        #self.timertext = gamefont.render('Timer:' +str(timer),1,[255,0,0])
        #self.boxsize = self.timertext.get_rect()
        #self.timerXpos = (640-self.boxsize[2])/2
        #screen.blit(self.timertext,[0,0])

        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
        # In case there is no sprite layer for the current map
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)
            #self.life.layers.append(self.objects) #추가한거
        # Initializing player sprite

            startCell1 = self.tilemap.layers['triggers'].find('playerStart')[random.randint(0,30)]
            self.player1 = character.Player((startCell1.px, startCell1.py), startCell1['playerStart'], self.players)
            startCell2 = self.tilemap.layers['triggers'].find('playerStart')[random.randint(0, 30)]
            self.player2 = character.Player2((startCell2.px, startCell2.py), startCell2['playerStart'], self.players)

            for i in range (0,9):
                startCell3 = self.tilemap.layers['triggers'].find('playerStart')[random.randint(0, 30)]
                self.player3 = character.NPC((startCell3.px, startCell3.py), startCell2['playerStart'],self.players)
            self.tilemap.layers.append(self.players)
            self.tilemap.set_focus(self.player1.rect.x, self.player1.rect.y) # 1p 시점



    def main(self):
        clock = pygame.time.Clock()
        self.initArea('ground.tmx')       ############# 배경 맵
        life = 5    # space 를 누를수 있는 횟수
        start_ticks = pygame.time.get_ticks()

        countdown = pygame.mixer.Sound('music/countdown (online-audio-converter.com).ogg')
        fall = pygame.mixer.Sound('music/arcade_game_fall_tone_003 (online-audio-converter.com).ogg')

        timer = 0
        win_1 = pygame.image.load('win_1.png')
        win_2 = pygame.image.load('win_2.png')
        display = pygame.display.set_mode((640,640))
        winActive = True
        #gamefont = pygame.font.Font(None,30)
        #timertext = gamefont.render('Timer:' +str(timer),1,[255,0,0])
        #win = gamefont.render('win',1,[0,255,0])
        #boxsize = timertext.get_rect()
        #timerXpos = (640-boxsize[2])/2
        #screen.blit(timertext,[timerXpos,50])


        while winActive:
            dt = clock.tick(30)  ###########30 프레임

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                    return
            #screen.blit(timertext,[timerXpos,50])
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # 얼마나 지났는지 초단위로 계산
            if seconds > 55:
                countdown.play()
            if seconds > 60:  # 3분 지날동안 2p 못잡으면 2p 승
                pygame.mixer.music.load('music/arcade_game_alarm_long.mp3')
                pygame.init()
                pygame.mixer.music.play()
                R.Act(winActive, win_2)
                winActive = False
                pygame.display.flip()




            self.tilemap.update(dt, self)
            screen.fill((0,0,0))
            self.tilemap.draw(self.screen)
            pygame.display.flip()
            self.pressed = pygame.key.get_pressed()

            key = pygame.key.get_pressed()
            distance12X = self.player1.rect.x - self.player2.rect.x    #1p 2p x좌표 차이
            distance12Y = self.player1.rect.y - self.player2.rect.y        # 1p 2p y좌표 차이

            if life >0 :        # life가 0 이상이면
                if key[pygame.K_SPACE]:
                    if(distance12X> -65 and distance12X <65):
                        if(distance12Y>-65 and distance12Y < 65):#  x y좌표 +-65 범위 안에 있으면
                            print("1p win")                 # 1p 우승 (이벤트 추가필요)
                            #이겼을때 event
                            pygame.mixer.music.load('music/little_robot_sound_factory_Jingle_Win_Synth_05.mp3')
                            pygame.init()
                            pygame.mixer.music.play()
                            R.Act(winActive,win_1)
                            winActive = False
                            pygame.display.flip()
                    else : fall.play() ; life -=1  ; print(life) ; pygame.display.flip()      # 라이프 -1  라이프 확인할수있게 프린트 써놨음
            else:
                pygame.mixer.music.load('music/arcade_game_alarm_long.mp3')
                pygame.init()
                pygame.mixer.music.play()
                R.Act(winActive,win_2)
                winActive = False
                pygame.display.flip()
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))

    timer = 0
    gamefont = pygame.font.Font(None, 30)

    pygame.display.set_caption("인터넷 응용 과제")
    Game(screen).main()

