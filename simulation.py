import sys
import pygame
from algo_classes import Utils


class Simulation:

    TROJANS = (156, 232, 255)
 
    def __init__(self, fly_in, screen, graph, nodes) -> None:
        self.screen = screen
        self.graph = graph
        self.nodes = nodes
        self.fly_in = fly_in
        wid, height = self.screen.get_size()
        self.controller_body = pygame.Rect(20, int(height * 0.20 - 10), int(wid * 0.60), int(height * 0.80 - 10))
        self.controller_l_antena = pygame.Rect(int(wid * 0.60 * 0.20), 20, 60, int(height * 0.20))
        self.controller_r_antena = pygame.Rect(int(wid * 0.60 * 0.70), 20, 60, int(height * 0.20))
        self.controller_screen = self.controller_body.inflate(-40, -250)
        self.controller_screen.y = int(height * 0.80 * 0.60)
        self.dashboard = pygame.Rect(int(wid * 0.60 + 40), 20, int(wid * 0.35), int(height * 0.95)) 

    def _draw_controller(self) -> None:
        pygame.draw.rect(self.screen, self.TROJANS, self.controller_body, border_radius=24)
        pygame.draw.rect(self.screen, self.TROJANS, self.controller_l_antena, border_radius=4)
        pygame.draw.rect(self.screen, self.TROJANS, self.controller_r_antena, border_radius=4)

        bezel = self.controller_screen.inflate(12, 12)
        pygame.draw.rect(self.screen, (0, 0, 0), bezel, border_radius=8)
        pygame.draw.rect(self.screen, (252, 251, 244), self.controller_screen, border_radius=4)
        
        jl = (self.controller_body.left + 120, self.controller_body.top + 120)
        jr = (self.controller_body.right - 120, self.controller_body.top + 120)
        pygame.draw.circle(self.screen, (0, 0, 0), jl, 60)
        pygame.draw.circle(self.screen, (50, 50, 50), jl, 30)
        pygame.draw.circle(self.screen, (0, 0, 0), jr, 60)
        pygame.draw.circle(self.screen, (50, 50, 50), jr, 30)

        bl1 = (self.controller_body.left + 300, self.controller_body.top + 80)
        bl2 = (self.controller_body.left + 250, self.controller_body.top + 160)
        br1 = (self.controller_body.right - 300, self.controller_body.top + 80)
        br2 = (self.controller_body.right - 250, self.controller_body.top + 160)
        pygame.draw.circle(self.screen, (0, 0, 0), bl1, 15)
        pygame.draw.circle(self.screen, (0, 0, 0), bl2, 15)
        pygame.draw.circle(self.screen, (0, 0, 0), br1, 15)
        pygame.draw.circle(self.screen, (0, 0, 0), br2, 15)
        
        center_button_start = (self.controller_body.left + 385, self.controller_body.top + 200)
        center_button_end = (self.controller_body.left + 455, self.controller_body.top + 200)
        pygame.draw.line(self.screen, (0, 0, 0), center_button_start, center_button_end, width=12)

    def _draw_dashboard(self) -> None:
        pygame.draw.rect(self.screen, self.TROJANS, self.dashboard, border_radius=24)
        title_font = pygame.font.SysFont("Comic Sans MS", 40)
        info_font = pygame.font.SysFont("Arial", 20)
        title_x = self.dashboard.left + 60
        title_y = self.dashboard.top + 10
        Utils.draw_text(self.screen, "Fly-In dashboard:", title_font, (0, 0, 0), title_x, title_y)
        info_x = self.dashboard.left + 10
        info_y = self.dashboard.top + 80
        Utils.draw_text(self.screen, f"- Map: {self.fly_in.map_file}", info_font, (0, 0, 0), info_x, info_y)
        Utils.draw_text(self.screen, f"- Nb of drones: {self.graph.nb_drones}", info_font, (0, 0, 0), info_x, info_y + 30)

    def run_step(self, events: list[str]) -> None:
        self.screen.fill((0, 0, 0))
        self._draw_controller()
        self._draw_dashboard()
