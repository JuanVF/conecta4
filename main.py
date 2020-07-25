import pygame

from gui.menu import Menu

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

menu = Menu(pygame)

menu.start_game()
