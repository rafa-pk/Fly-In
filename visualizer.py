import pygame
import os

class Visualizer:
    
    def __init__(self, screen, program) -> None:
        """init method for the visualizer class"""
        self.screen = screen
        self.program = program
        self.menu_title_font = pygame.font.SysFont("Arial", 60)
        self.options_font = pygame.font.SysFont("Arial", 30)
        self.menu_path = './maps'
        self.menu_index = 0

    def draw_text(self, text: str, font: str, color: tuple[int, int, int],
                  x: int, y: int) -> None:
        """method to draw text to screen"""
        image = font.render(text, True, color)
        self.screen.blit(image, (x, y))
           
    def maps_menu(self, events: list[str, ...]) -> str:
        """method which handles the menu when the program launches"""
        contents = os.listdir(self.menu_path)
        for event in events:
            if event.type == pygame.QUIT:
                self.program.status(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.program.status(False)
                if event.key in (pygame.K_UP, pygame.K_k):
                    self.menu_index = (self.menu_index - 1) % len(contents)
                if event.key in (pygame.K_DOWN, pygame.K_j):
                    self.menu_index = (self.menu_index + 1) % len(contents)
                if event.key == pygame.K_RETURN:
                    selected = contents[self.menu_index]
                    full_path = os.path.join(self.menu_path, selected)
                    if os.path.isdir(full_path):
                        self.menu_path = full_path
                        self.menu_index = 0
                    else:
                        return full_path
        
        self.screen.fill((0, 0, 0))
        self.draw_text("Select your desired map file:", self.menu_title_font, 
                       (250, 250, 250), 300, 50)
        ix = 0
        offset = 50
        for element in contents:
            entry = f"[{ix}]: {element}"
            self.draw_text(entry, self.options_font, (250, 250, 250),
                           500, 100 + offset)
            ix += 1
            offset += 70
        #if enter is clicked, return the name of that file as a str
