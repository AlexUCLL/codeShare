from operator import ne
import pygame

class Spaceship:
    # initial position is blit + (25,27)
    def __init__(self) -> None:
        self.__image = pygame.image.load('Images/player_sprite.png').convert_alpha()
        self.__xco = 487
        self.__yco = 656
        self.speed=400
        self.hitbox=(self.__xco+50, self.__yco+55)

    @property
    def xco(self):
        return self.__xco
    
    @property
    def yco(self):
        return self.__yco

    def up(self, elapsed_seconds):
        if(self.__yco-self.speed*elapsed_seconds)>0:
            self.__yco-=self.speed*elapsed_seconds
    def down(self, elapsed_seconds):
        if(self.__yco+self.speed*elapsed_seconds)<768:
            self.__yco += self.speed*elapsed_seconds
    def left(self, elapsed_seconds):
        if(self.__xco-self.speed*elapsed_seconds)>0:
                self.__xco -=self.speed*elapsed_seconds
    def right(self, elapsed_seconds):
            if(self.__xco+self.speed*elapsed_seconds)<1024:
                self.__xco +=self.speed*elapsed_seconds
    

    def render(self, surface):
         surface.blit(self.__image, (self.__xco-25, self.__yco-27))
    