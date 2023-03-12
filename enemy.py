from random import randint
import pygame


class Enemy:
    def __init__(self, xco, yco) -> None:
        self.__xco=xco
        self.__yco=yco
        self.dead=False
        self.disposed=False
        self.__random=randint(1,4)
        self.__sprite=pygame.image.load( "Images/sprites/enemy"+str(self.__random)+".png").convert_alpha()
        if(self.__random==1 or self.__random==3): 
            self.__speed=30
            self.__ttl=50
            if(self.__random==1):
                self.hitbox=(xco+75,yco+76)
                self.score=40
            else:
                self.hitbox=(xco+125,yco+238)
                self.score=30
        elif(self.__random==2 or self.__random==4):
            self.__speed=15
            self.__ttl=100
            if(self.__random==2):
                self.hitbox=(xco+100, yco+102)
                self.score=10
            else:
                self.hitbox=(xco+57, yco+60)
                self.score=20
    @property
    def x(self):
        return self.__xco
    @property
    def y(self):
        return self.__yco

    def render(self, surface):        
        surface.blit(self.__sprite, (self.__xco, self.__yco))
    
    def update(self, elapsed_seconds):
        self.__yco+= (self.__speed*elapsed_seconds)
        if(self.__random==1):
            self.hitbox=(self.__xco+75,self.__yco+76)
        elif(self.__random==2):
            self.hitbox=(self.__xco+100, self.__yco+102)
        elif(self.__random==3):
            self.hitbox=(self.__xco+125,self.__yco+238)
        else:
            self.hitbox=(self.__xco+57, self.__yco+60)  
        self.__ttl-=elapsed_seconds
        if(self.__ttl<=0):
            self.disposed=True

