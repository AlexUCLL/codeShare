import pygame


pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()
clock = pygame.time.Clock()
print(controller.get_numaxes())
#controller.rumble(1,10,20)
while True:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN and event.button == 7:
            print(f'Exiting controller loop')
            done = True

    #for i in range(controller.get_numaxes()):
        print(f'Axis {1}: {controller.get_axis(1)}')

    #for i in range(controller.get_numbuttons()):
        button = controller.get_button(0)
        print("Button {:>2} value: {}".format(0, button))
    # pygame.display.flip()

    clock.tick()