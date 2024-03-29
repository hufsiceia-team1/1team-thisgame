import pygame



class Player(pygame.sprite.Sprite):  # 캐릭터
    def __init__(self, location, orientation, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('sprites/player5.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64, 64))
        self.orient = orientation
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        # Set default orientation
        self.setSprite()

    def setSprite(self):  ###########################방향 전환
        # Resets the player sprite sheet to its default position
        # and scrolls it to the necessary position for the current orientation
        self.image = self.imageDefault.copy()
        if self.orient == 'left':
            self.image.scroll(0, -64)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'right':
            self.image.scroll(0, -128)
        elif self.orient == 'up':
            self.image.scroll(0, -192)

    def update(self, dt, game):
        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input:

        if key[pygame.K_UP]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_DOWN]:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_LEFT]:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_RIGHT]:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()

                self.holdTime += dt

        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 100:
            self.walking = True
        lastRect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing
        if self.walking and self.dx < 64:


            if self.orient == 'up':
                self.rect.y -= 4
            elif self.orient == 'down':
                self.rect.y += 4
            elif self.orient == 'left':
                self.rect.x -= 4
            elif self.orient == 'right':
                self.rect.x += 4
            self.dx += 4
        # Collision detection:
        # Reset to the previous rectangle if player collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect,  ###################  고체 trigger랑 부딪히면
                                                       'solid')) > 0:
            self.rect = lastRect


            return
        # Switch to the walking sprite after 32 pixels
        if self.dx == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or
                self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.dx == 64:
            self.walking = False
            self.setSprite()
            self.dx = 0
        game.tilemap.set_focus(self.rect.x, self.rect.y)  #####################걷는 방향에 맞춰 스크린 움직임
        #print(self.rect.x,self.rect.y)


class Player2(Player):  # 1p로부터 오버라이딩
    def update(self, dt, game):
        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input:
        if key[pygame.K_w]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_s]:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_a]:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_d]:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()
                self.holdTime += dt

        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 100:
            self.walking = True
        lastRect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing
        if self.walking and self.dx < 64:
            if self.orient == 'up':
                self.rect.y -= 8
            elif self.orient == 'down':
                self.rect.y += 8
            elif self.orient == 'left':
                self.rect.x -= 8
            elif self.orient == 'right':
                self.rect.x += 8
            self.dx += 8
        # Collision detection:
        # Reset to the previous rectangle if player collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect,  ###################  고체 trigger랑 부딪히면
                                                       'solid')) > 0:

            self.rect = lastRect


            return
        # Switch to the walking sprite after 32 pixels
        if self.dx == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or
                self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.dx == 64:
            self.walking = False
            self.setSprite()
            self.dx = 0

class NPC(Player):  # 1p로부터 오버라이딩

    def update(self, dt, game):
        import random
        import time
        movement = ['up','down','left','right']
        randomMove = random.choice(movement)

        if randomMove =='up':
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
        elif randomMove =='down':
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()
                self.holdTime += dt
        elif randomMove =='left':
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                self.holdTime += dt
        elif randomMove =='right':
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()
                self.holdTime += dt
        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 100:
            self.walking = True
        lastRect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing


        if self.walking and self.dx < 64:
            if self.orient == 'up':
                self.rect.y -= 8

            elif self.orient == 'down':
                self.rect.y += 8

            elif self.orient == 'left':
                self.rect.x -= 8

            elif self.orient == 'right':
                self.rect.x += 8

            self.dx += 8

        # Collision detection:
        # Reset to the previous rectangle if player collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect,  ###################  고체 trigger랑 부딪히면
                                                       'solid')) > 0:
            self.rect = lastRect



            return
        # Switch to the walking sprite after 32 pixels
        if self.dx == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or
                self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.dx == 64:
            self.walking = False
            self.setSprite()
            self.dx = 0
        #print(self.rect.x,self.rect.y)
class distance():
    def __init__(self, player1, object):
        self.Xdistance = player1.rect.x - object.rect.x
        self.Ydistance = player1.rect.y - object.rect.y
        print(self.Xdistance,self.Ydistance)
