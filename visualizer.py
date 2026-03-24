import pygame
import os

class Visualizer:
    
    def __init__(self, screen, program) -> None:
        """init method for the visualizer class"""
        self.screen = screen
        self.program = program
        self.menu_title_font = pygame.font.SysFont("Arial", 60)
        self.options_font = pygame.font.SysFont("Arial", 30)

    def draw_text(self, text: str, font: str, color: tuple[int, int, int],
                  x: int, y: int) -> None:
        """method to draw text to screen"""
        image = font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def menu_keys_handling(self, key_flag, contents: list[str, ...]) -> int:
        mp = 0

        if key_flag == pygame.K_UP or pygame.K_k:
            if mp + 1 > len(contents):
                mp = 0
            else:
                mp += 1
        elif key_flag == pygame.K_DOWN or pygame.K_j:
            if mp - 1 < 0:
                mp = len(contents)
            else:
                mp -= 1
        return mp
            

    def maps_menu(self, events: list[str, ...]) -> str:
        """method which handles the menu when the program launches"""
        for event in events:
            if event.type == pygame.QUIT:
                self.program.status(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.program.status(False)
                index = self.menu_keys_handling(event.key, contents)
                if event.key == pygame.K_RETURN:
                    if os.path.isdir(contents[index]):
                        path += f"/{contents[index]}"
                        contents = os.listdir(path)
                    else:
                        return contents[index]
        path = './maps'
        contents = os.listdir(path)
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
        

        return None
        #implement navigation (key hooks + color change)
        #if dir -> go in dir
        #if enter is clicked, return the name of that file as a str
