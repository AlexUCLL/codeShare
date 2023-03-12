import pygame


class Bullet:
    def __init__(self, xco, yco) -> None:
        self.__image=pygame.image.load("Images/sprites/bullets/small.png")
        self.__x=(xco)
        self.__y=(yco)
        self.hitbox=(self.__x, self.__y)
        self.__speed=(20)
        self.__time_left=(50)
        self.disposed=False
    
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    def render(self, surface):
        surface.blit(self.__image, (self.__x,self.__y))
    def update(self, elapsed_seconds):
        self.__y-= (self.__speed*elapsed_seconds)
        self.hitbox=(self.__x, self.__y)
        self.__time_left-=elapsed_seconds
        if(self.__time_left<=0):
            self.disposed=True
