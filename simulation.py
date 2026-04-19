import sys
import pygame


class Simulation:

    CONTROLLER_BODY = (156, 232, 255)
 
    def __init__(self, screen, graph, nodes) -> None:
        self.screen = screen
        self.graph = graph
        self.nodes = nodes
        wid, height = self.screen.get_size()
        self.controller = pygame.Rect(0, 0, int(wid * 0.70), int(height * 0.20))
        self.dashboard = pygame.Rect(int(wid * 0.75), int(height - 10), int(wid * 20), int(height - 20)) 

    def _draw_controller(self) -> None:
        pygame.draw.rect(self.screen, self.CONTROLLER_BODY, self.controller, border_radius=24)


    def run_step(self, events: list[str]) -> None:
        self.screen.fill((0, 0, 0))
        self._draw_controller()