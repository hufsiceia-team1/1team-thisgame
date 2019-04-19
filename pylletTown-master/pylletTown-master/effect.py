import pygame

class render():
    def Act(self,Active,img):
        display = pygame.display.set_mode((640, 640))
        while Active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Active = False
            display.blit(img, [0, 0])
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                Active = False
            pygame.display.flip()