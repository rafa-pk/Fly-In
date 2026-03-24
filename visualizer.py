import pygame
import os

class Visualizer:
    
    def __init__(self, screen) -> None:
        self.screen = screen
        self.menu_title_font = pygame.font.SysFont("Arial", 30)
        self.options_font = pygame.font.SysFont("Arial", 20)

    def draw_text(self, text: str, font: str, color: tuple[int, int, int],
                  x: int, y: int) -> None:
        image = font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def maps_menu(self) -> str:
        offset = 50
        self.draw_text("Select your desired map file:", self.menu_title_font, 
                       (250, 250, 250), 500, 50)
        contents = os.listdir('./maps/easy')
        ix = 0
        for element in contents:
            entry = f"[{ix}]: {element}"
            self.draw_text(entry, self.options_font, (250, 250, 250),
                           600, 100 + offset)
            ix += 1
            offset += 50
        

        return ""
        #implement navigation (key hooks + color change)
        #if dir -> go in dir
        #if enter is clicked, return the name of that file as a str
