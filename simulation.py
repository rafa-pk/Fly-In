import sys
import os
import pygame
from algo_classes import Utils


class Simulation:

    TROJANS = (156, 232, 255)
    EDGE = (255, 242, 175)
 
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
        self.dashboard_term = self.dashboard.inflate(-40, -220)
        self.dashboard_term.y = int(height * 0.35 * 0.80)

        xs = [n.x for n in self.graph.nodes.values()]
        ys = [n.y for n in self.graph.nodes.values()]
        self.real_minx, self.real_maxx = min(xs), max(xs)
        self.real_miny, self.real_maxy = min(ys), max(ys)
        g_width = self.real_maxx - self.real_minx or 1
        g_height = self.real_maxy - self.real_miny or 1
        padding = 40
        padded_window_w = self.controller_screen.width - padding * 2
        padded_window_h = self.controller_screen.height - padding * 2
        self.scale = min(padded_window_w / g_width, padded_window_h / g_height)

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
        
        logo = pygame.image.load("assets/logo.png")
        center_button_start = (self.controller_body.left + 385, self.controller_body.top + 200)
        center_button_end = (self.controller_body.left + 455, self.controller_body.top + 200)
        self.screen.blit(logo, (self.controller_body.left + 300, self.controller_body.top))
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
        dirname = os.path.dirname(self.fly_in.map_file)
        if "easy" in dirname:
            difficulty = "easy"
        elif "medium" in dirname:
            difficulty = "medium"
        elif "hard" in dirname:
            difficulty = "hard"
        elif "challenger" in dirname:
            difficulty = "challenger"
        Utils.draw_text(self.screen, f"- Difficulty: {difficulty}", info_font, (0, 0, 0), info_x, info_y + 60)
        pygame.draw.rect(self.screen, (0, 0, 0), self.dashboard_term, border_radius=2)
        term_header_x = self.dashboard_term.x + 10
        term_header_y = self.dashboard_term.y + 10
        term_font = pygame.font.SysFont("Microsoft Sans Serif", 13)
        Utils.draw_text(self.screen, "rvaz-da-@simulation fly_in  % python3 fly_in.py", term_font, (250, 250, 250), term_header_x, term_header_y)

    def _transform_coords(self, x: int, y: int) -> tuple[int, int]:
        screen_cx = (self.real_minx + self.real_maxx) / 2
        screen_cy = (self.real_miny + self.real_maxy) / 2
        screen_x = self.controller_screen.centerx + (x - screen_cx) * self.scale
        screen_y = self.controller_screen.centerx + (y - screen_cy) * self.scale
        return (int(screen_x), int(screen_y))

    def _draw_graph(self) -> None:
        nodes = self.graph.nodes
        drawn = set()
        
        for node_name, edge_list in self.graph.connections.items():
            for edge in edge_list:
                key = tuple(sorted(edge.connection))
                if key in drawn:
                    continue
                drawn.add(key)

                n1 = self.graph.nodes[edge.connection[0]]
                n2 = self.graph.nodes[edge.connection[1]]
                pygame.draw.line(
                    self.screen, self.EDGE,
                    self._transform_coords(n1.x, n1.y),
                    self._transform_coords(n2.x, n2.y),
                    4,
                )
        for node in nodes:
            node_o = self.graph.nodes[node]
            nx, ny = self._transform_coords(node_o.x, node_o.y)
            pygame.draw.circle(self.screen, node_o.color, (nx, ny), 20) 

    #def _animate_step(self) -> None:


    def run_step(self, events: list[str]) -> None:
        self.screen.fill((0, 0, 0))
        self._draw_controller()
        self._draw_dashboard()
        self._draw_graph()
        #self._animate_step()
