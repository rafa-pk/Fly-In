import pygame
import os

class FileMenu:
    
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
    
    def draw_text_box(self, text: str, text_color: tuple[int, int, int], 
                  font: str, bg_color: tuple[int, int, int],
                  x: int, y: int, padding: int) -> None:
        """method to draw text to screen with bg underneath"""
        image = font.render(text, True, text_color)
        text_box = image.get_rect(topleft=(x,y))
        bg_rect = pygame.Rect(text_box.x - padding, text_box.y - padding, 
                              text_box.width + padding*2, text_box.height + padding*2)
        pygame.draw.rect(self.screen, bg_color, bg_rect, 0)
        self.screen.blit(image, (x, y))

       
    def menu(self, events: list[str, ...]) -> str:
        """method which handles the menu when the program launches"""
        try:
            contents: list[str, ...] = os.listdir(self.menu_path)
        except Exception as error:
            print(f"Error: Map menu: {error}")
        highlight_menu_entry: bool = True
        for event in events:
            if event.type == pygame.QUIT:
                self.program.status(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.program.status(False)
                if event.key in (pygame.K_UP, pygame.K_k):
                    self.menu_index = (self.menu_index - 1) % len(contents)
                    highlight_menu_entry = True
                if event.key in (pygame.K_DOWN, pygame.K_j):
                    self.menu_index = (self.menu_index + 1) % len(contents)
                    highlight_menu_entry = True
                if event.key in (pygame.K_LEFT, pygame.K_h):
                    try:
                        if os.path.isdir(self.menu_path) and self.menu_path != "./maps":
                            parent_dir = os.path.dirname(self.menu_path)
                            if parent_dir != self.menu_path:
                                self.menu_path = parent_dir
                                self.menu_index = 0
                    except Exception as error:
                        print(f"Error: Menu navigation: {error}")
                if event.key in (pygame.K_RETURN, pygame.K_RIGHT, pygame.K_l):
                    try:
                        selected = contents[self.menu_index]
                        full_path = os.path.join(self.menu_path, selected)
                        if os.path.isdir(full_path):
                            self.menu_path = full_path
                            self.menu_index = 0
                        elif event.key == pygame.K_RETURN:
                            return full_path
                    except Exception as error:
                        print(f"Error: Menu navigation: {error}")
        
        self.screen.fill((0, 0, 0))
        try:
            self.draw_text("Select your desired map file:", self.menu_title_font, 
                           (250, 250, 250), 300, 50)
            ix = 0
            offset = 50
            for i, element in enumerate(contents):
                entry = f"  [{ix}]:  {element}"
                pygame.draw.line(self.screen, (51, 51, 51), (0, 80 + offset), 
                                 (self.screen.get_width(), 80 + offset), 1)
                if highlight_menu_entry and i == self.menu_index:
                    self.draw_text_box(entry, (250, 250, 250), self.options_font,
                                       (51, 51, 51), 0, 100 + offset, 0)
                    highlight_menu_entry = False
                else:
                    self.draw_text(entry, self.options_font, (250, 250, 250),
                                   0, 100 + offset)
                ix += 1
                offset += 70
            pygame.draw.line(self.screen, (51, 51, 51), (0, 80 + offset), 
                                 (self.screen.get_width(), 80 + offset), 1)
        except Exception as error:
            print(f"Visualization error: Option menu: {error}")
            sys.exit(1)
