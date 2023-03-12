from random import randint
import pygame
import math
from audio.sound import SoundLibrary
from bullet import Bullet
from enemy import Enemy
from looping import looping_variable
from spaceship import Spaceship
from cooldown import Cooldown

# Initialize Pygame
pygame.init()


# Colors

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

def create_main_surface():
    # Tuple representing width and height in pixels
    screen_size = (1024, 768)

# Create window with given size
    return pygame.display.set_mode(screen_size)

# Clear surface
def clear_surface(surface):
    surface.fill((0,0,0,0))

pygame.display.set_caption("Focking Sick Bootleg Galaga")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    surface = create_main_surface()
    screen_text = font.render(text, True, color)
    surface.blit(screen_text, [x,y])

# Welcome function
def welcome():
    surface = create_main_surface()
    status = State()
    pygame.mixer.music.load("./music/BOSSMUSIC.mp3")
    pygame.mixer.music.play(-1)

    exit_game = False
    while not exit_game:
        surface.fill((0,0,0))
        surface.blit(pygame.image.load("Images/welcome.png"), (0, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.fadeout(2000)
                    pygame.mixer.music.unload()
                    main()

        pygame.display.update()
        clock.tick(60)

# Main function
def main():
    surface = create_main_surface()
    status = State()
    clang = pygame.time.Clock()
    spawn_timer = 0
    pygame.mixer.music.load("./music/Raining Blood.mp3")
    pygame.mixer.music.play(-1)
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, ])
    pygame.joystick.init()
    while not status.dead:
        elapsed_seconds = clang.tick()/1000
        clear_surface(surface)
        spawn_timer+=1
        if(spawn_timer>10):
            status.spawn_enemy()
            spawn_timer=0
        status.render(surface)
        status.process_key_input(pygame.key.get_pressed(), elapsed_seconds)
        if(pygame.joystick.get_count()>=1):
            status.process_controller_input(elapsed_seconds)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                exit()
        status.update(elapsed_seconds)
    game_over(status.score)

def game_over(score):
    surface = create_main_surface()
    restart = False
    pygame.mixer.music.load("./music/YOU_DIED_HD.mp3")
    pygame.mixer.music.play()
    while not restart:
        surface.fill((0,0,0))
        surface.blit(pygame.image.load("Images/gameOver.png"), (0, 50))
        my_font = pygame.font.SysFont(None, 50)
        score_string="Score: {}".format(score)
        text_surface = my_font.render(score_string, True, (255, 255, 255))
        surface.blit(text_surface, (10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()        
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                restart=True
        pygame.display.update()
        clock.tick(60)
    welcome()
    

# State class that keeps track of the game's State
class State:
    def __init__(self) -> None:
        self.xco=0
        self.yco=0
        self.__bockground = Background()
        self.__spaceship = Spaceship()
        self.__sound_library = SoundLibrary()
        self.__bullets = []
        self.__cooldown = Cooldown(6)
        self.__enemies=[]
        self.dead=False
        self.__score=0
        if(pygame.joystick.get_count()>=1):
            self.__controller = pygame.joystick.Joystick(0)
            self.__controller.init()
    
    @property
    def score(self):
        return self.__score

    @property
    def spaceship(self):
        return self.__spaceship

    def update(self, elapsed_time) -> None:
        self.__bockground.update(elapsed_seconds = math.ceil(elapsed_time))
        self.__cooldown.update(elapsed_seconds=math.ceil(elapsed_time))
        for enemy in self.__enemies:
            for bullet in self.__bullets:
               if self.collision_check(enemy.x, enemy.y, enemy.hitbox, bullet.x, bullet.y, bullet.hitbox):
                   self.__sound_library.play_random_explosion()
                   enemy.dead=True
                   bullet.disposed=True
            enemy.update(elapsed_seconds = math.ceil(elapsed_time))
            if(enemy.dead):
                self.__score+=enemy.score
                self.__enemies.remove(enemy)
            if enemy.disposed:
                self.__enemies.remove(enemy)
            if self.collision_check(enemy.x, enemy.y, enemy.hitbox, self.__spaceship.xco, self.__spaceship.yco, self.__spaceship.hitbox):
                self.dead=True
        for bullet in self.__bullets:
            bullet.update(elapsed_seconds = math.ceil(elapsed_time))
            if(bullet.disposed):
                self.__bullets.remove(bullet)
            
    def render(self, surface) -> None:
        self.__bockground.render(surface)
        for bullet in self.__bullets:
            bullet.render(surface)
        for enemy in self.__enemies:
            enemy.render(surface)
        self.__spaceship.render(surface)
        my_font = pygame.font.SysFont(None, 50)
        score="Score: {}".format(self.__score)
        text_surface = my_font.render(score, True, (255, 255, 255))
        surface.blit(text_surface, (10, 10))
        pygame.display.flip()
    
    def spawn_enemy(self):
        self.__enemies.append(Enemy(randint(10,970), -10))
    
    def collision_check(self, x1, y1, box1, x2, y2, box2):
        if(x1<x2 and x2<=box1[0]):
            if(y1<y2 and y2<=box1[1]):
                return True
            if(y1<box2[1] and box2[1]<=box1[1]):
                return True
        if(x2<x1 and y2<y1 and x2>=box1[0] and y2>=box1[1]):
            return True
        return False
    def process_controller_input(self, elapsed_seconds):
        if self.__controller.get_axis(0)<-0.3:
            self.spaceship.left(elapsed_seconds)
        if self.__controller.get_axis(0)>0.3:
            self.spaceship.right(elapsed_seconds)
        if self.__controller.get_axis(1)<-0.3:
            self.__spaceship.up(elapsed_seconds)
        if self.__controller.get_axis(1)>0.3:
            self.__spaceship.down(elapsed_seconds)
        if self.__controller.get_button(0)==1:
            if(self.__cooldown.ready):
                self.__bullets.append(Bullet(self.spaceship.xco-9, self.spaceship.yco-9))
                self.__sound_library.table["/shots/laser"].play()
                self.__cooldown.reset()

    def process_key_input(self, key, elapsed_seconds):
        if key[pygame.K_DOWN]:
            self.spaceship.down(elapsed_seconds)
        if key[pygame.K_UP]:
            self.spaceship.up(elapsed_seconds)
        if key[pygame.K_RIGHT]:
            self.spaceship.right(elapsed_seconds)
        if key[pygame.K_LEFT]:
            self.spaceship.left(elapsed_seconds)
        if key[pygame.K_SPACE]:
            if(self.__cooldown.ready):
                self.__bullets.append(Bullet(self.spaceship.xco-9, self.spaceship.yco-9))
                self.__sound_library.table["/shots/laser"].play()
                self.__cooldown.reset()

class Background:
    def __init__(self) -> None:
        self.bgimage = self.__create_image()
        self.rectBGimg = self.bgimage.get_rect()
        self.pos=looping_variable(3553)
    def __create_image(self):
        return pygame.image.load("Images/background.png").convert()
    
    #def __goDown(self):
        #self.yco+=5
    def flip_image_vertically(self):
        return pygame.transform.flip(self.bgimage, False, True)

    def render(self, surface):
            surface.blit(self.bgimage,(0,self.pos.value))
            surface.blit(self.flip_image_vertically(),(0,self.pos.value - self.pos.max_value))   

    def update(self,elapsed_seconds):
            self.pos.increase(elapsed_seconds*10)



welcome()