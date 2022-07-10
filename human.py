import game_interface
from game_interface import pygame

game_interface.burger_dog.reset()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the Surface
    game_interface.update_display()

    # Handle Player Events
    action = [0,0,0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        action[0] = -1
    elif keys[pygame.K_RIGHT]:
        action[0] = 1
        
    if keys[pygame.K_UP]:
        action[1] = -1
    elif keys[pygame.K_DOWN]:
        action[1] = 1

    if keys[pygame.K_SPACE]:
        action[2] = 1
    
    
    game_interface.step(action)
    
