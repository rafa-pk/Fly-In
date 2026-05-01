import os
import pygame
import random
import webbrowser
from algo_classes import Utils


class Simulation:

    TROJANS = (156, 232, 255)
    EDGE = (255, 242, 175)
    MAX_VISIBLE_LINES = 34

    def __init__(self, fly_in, screen, graph, drones) -> None:
        self.screen = screen
        self.graph = graph
        self.drones = drones
        self.fly_in = fly_in
        wid, height = self.screen.get_size()
        self.controller_body = pygame.Rect(20, int(height * 0.20 - 10),
                                           int(wid * 0.60),
                                           int(height * 0.80 - 10))
        self.controller_l_antena = pygame.Rect(int(wid * 0.60 * 0.20), 20, 60,
                                               int(height * 0.20))
        self.controller_r_antena = pygame.Rect(int(wid * 0.60 * 0.80), 20, 60,
                                               int(height * 0.20))
        self.controller_screen = self.controller_body.inflate(-40, -250)
        self.controller_screen.y = int(height * 0.80 * 0.60)
        self.dashboard = pygame.Rect(int(wid * 0.60 + 40), 20, int(wid * 0.35),
                                     int(height * 0.95))
        self.dashboard_term = self.dashboard.inflate(-40, -220)
        self.dashboard_term.y = int(height * 0.35 * 0.80)
        self.screamer_active = False
        self.fah = pygame.mixer.Sound("sfx/FAH.mp3")

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
        self._relative_node_coords: dict[str, tuple[int, int]] = {}

        self.sim_t = 0
        self.accumulator = 0.0
        self.step_duration = 1
        self.paused = False
        self.drone_img = pygame.image.load("assets/drone.png")
        self.drone_img = pygame.transform.smoothscale(self.drone_img, (20, 20))
        self.moves = 0
        self.log_lines: list[str] = []
        self._to_draw_info: tuple[str, int, int] = ()

    def _draw_info(self, node_coords: tuple[str, int, int]) -> None:
        node, nx, ny = node_coords
        title_font = pygame.font.SysFont("Arial", 30)
        info_rect = pygame.Surface((300, 210), pygame.SRCALPHA)
        info_rect.fill((133, 133, 133, 250))
        node = self.graph.nodes[node]
        tx = 5
        ty = 50
        ofs = 0
        Utils.draw_text(info_rect, "Hub Info:", title_font, (0, 0, 0), 80, 5)
        text_font = pygame.font.SysFont("Arial", 20)
        connections = {edge.connection for edge
                       in self.graph.connections[node.name]}
        text = {
            "Name: ": node.name,
            "Type: ": node.type.value,
            "Zone: ": node.zone.value,
            "Max drones: ": node.max_drones,
            "Connections: ": len(connections)
            }
        for title, info in text.items():
            Utils.draw_text(info_rect, f"{title}{info}", text_font, (0, 0, 0),
                            tx, ty + ofs)
            ofs += 30
        self.screen.blit(info_rect, (nx + 5, ny - 220))

    def _handle_events(self, events: list[str]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.fly_in.status(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.fly_in.status(False)
                if event.key == pygame.K_x:
                    if self.screamer_active:
                        self.screamer_active = False
                if event.key == pygame.K_SPACE:
                    if not self.paused:
                        self.paused = True
                    else:
                        self.paused = False
                if event.key == pygame.K_r:
                    self.fly_in.state = "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                try:
                    if self.magic_button.collidepoint(pos):
                        res = webbrowser.open_new("https://www.youtube.com/wat"
                                                  "ch?v=xvFZjo5PgG0")
                        if not res:
                            raise RuntimeError("Magic button did not work :(")
                    elif self.magic_button2.collidepoint(pos):
                        faces = ["wkhattab", "mbucci", "rpousseu", "hmesnard"]
                        chosen = random.choice(faces)
                        self.screamer = pygame.image.load(f"assets/"
                                                          f"{chosen}.png")
                        scale = self.screen.get_size()
                        self.screamer = pygame.transform.scale(self.screamer,
                                                               scale)
                        self.screamer_active = True
                    else:
                        self.fah.play()
                except Exception as message:
                    print(f"{message}")
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                hit_radius = 10
                for node, (nx, ny) in self._relative_node_coords.items():
                    if (mx - nx) ** 2 + (my - ny) ** 2 <= hit_radius ** 2:
                        self._to_draw_info = (node, nx, ny)
                        break
                else:
                    self._to_draw_info = ()

    def _draw_controller(self) -> None:
        pygame.draw.rect(self.screen, self.TROJANS, self.controller_body,
                         border_radius=24)
        pygame.draw.rect(self.screen, self.TROJANS, self.controller_l_antena,
                         border_radius=4)
        pygame.draw.rect(self.screen, self.TROJANS, self.controller_r_antena,
                         border_radius=4)

        bezel = self.controller_screen.inflate(12, 12)
        pygame.draw.rect(self.screen, (0, 0, 0), bezel, border_radius=8)
        pygame.draw.rect(self.screen, (252, 251, 244), self.controller_screen,
                         border_radius=4)
        font = pygame.font.SysFont("Microsoft Sans Serif", 15)
        lx = self.controller_screen.x + 10
        ly = 720
        Utils.draw_text(self.screen, "Controls: ", font, (0, 0, 0), lx, ly)
        Utils.draw_text(self.screen, "<space> - pause/resume simulation     "
                        "<r> - restart program from start", font, (0, 0, 0),
                        lx, ly + 20)

        jl = (self.controller_body.left + 120, self.controller_body.top + 120)
        jr = (self.controller_body.right - 120, self.controller_body.top + 120)
        pygame.draw.circle(self.screen, (0, 0, 0), jl, 60)
        pygame.draw.circle(self.screen, (50, 50, 50), jl, 30)
        pygame.draw.circle(self.screen, (0, 0, 0), jr, 60)
        pygame.draw.circle(self.screen, (50, 50, 50), jr, 30)

        bl1 = (self.controller_body.left + 300, self.controller_body.top + 80)
        bl2 = (self.controller_body.left + 250, self.controller_body.top + 160)
        br1 = (self.controller_body.right - 300, self.controller_body.top + 80)
        br2 = (self.controller_body.right - 250,
               self.controller_body.top + 160)
        self.magic_button = pygame.Rect(br1[0] - 15, br1[1] - 15, 15 * 2,
                                        15 * 2)
        self.magic_button2 = pygame.Rect(jl[0] - 30, jl[1] - 30, 30 * 2,
                                         30 * 2)
        pygame.draw.circle(self.screen, (0, 0, 0), bl1, 15)
        pygame.draw.circle(self.screen, (0, 0, 0), bl2, 15)
        pygame.draw.circle(self.screen, (0, 0, 0), br1, 15)
        pygame.draw.circle(self.screen, (0, 0, 0), br2, 15)

        logo = pygame.image.load("assets/logo.png")
        logo = pygame.transform.scale(logo, (90, 90))
        center_button_start = (self.controller_body.left + 385,
                               self.controller_body.top + 200)
        center_button_end = (self.controller_body.left + 455,
                             self.controller_body.top + 200)
        self.screen.blit(logo, (self.controller_body.left + 370,
                                self.controller_body.top + 20))
        pygame.draw.line(self.screen, (0, 0, 0), center_button_start,
                         center_button_end, width=12)

    def _wrap_line(self, line: str, font: pygame.font.Font,
                   max_width: int) -> list[str]:
        entries = line.split(' ')
        lines = []
        current = ""

        for entry in entries:
            candidate = entry if not current else current + " " + entry
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = entry
        if current:
            lines.append(current)
        return lines

    def _draw_dashboard(self) -> None:
        pygame.draw.rect(self.screen, self.TROJANS, self.dashboard,
                         border_radius=24)
        title_font = pygame.font.SysFont("Comic Sans MS", 40)
        info_font = pygame.font.SysFont("Arial", 20)
        title_x = self.dashboard.left + 60
        title_y = self.dashboard.top + 10
        Utils.draw_text(self.screen, "Fly-In dashboard:", title_font,
                        (0, 0, 0), title_x, title_y)
        info_x = self.dashboard.left + 10
        info_y = self.dashboard.top + 80
        Utils.draw_text(self.screen, f"- Map: {self.fly_in.map_file}",
                        info_font, (0, 0, 0), info_x, info_y)
        Utils.draw_text(self.screen, f"- Nb of drones: {self.graph.nb_drones}",
                        info_font, (0, 0, 0), info_x, info_y + 30)
        dirname = os.path.dirname(self.fly_in.map_file)
        if "easy" in dirname:
            difficulty = "easy"
        elif "medium" in dirname:
            difficulty = "medium"
        elif "hard" in dirname:
            difficulty = "hard"
        elif "challenger" in dirname:
            difficulty = "challenger"
        Utils.draw_text(self.screen, f"- Difficulty: {difficulty}", info_font,
                        (0, 0, 0), info_x, info_y + 60)
        Utils.draw_text(self.screen, f"- Moves: {self.moves}", info_font,
                        (0, 0, 0), info_x, info_y + 90)
        pygame.draw.rect(self.screen, (0, 0, 0), self.dashboard_term,
                         border_radius=2)
        term_header_x = self.dashboard_term.x + 10
        term_header_y = self.dashboard_term.y + 10
        term_font = pygame.font.SysFont("Microsoft Sans Serif", 13)
        Utils.draw_text(self.screen, "rvaz-da-@simulation fly_in  % "
                        "python3 fly_in.py", term_font, (250, 250, 250),
                        term_header_x, term_header_y)
        offset = 15
        visual_lines = []
        for line in self.log_lines:
            visual_lines.extend(self._wrap_line(line, term_font,
                                self.dashboard_term.width))
        for subline in visual_lines[-self.MAX_VISIBLE_LINES:]:
            Utils.draw_text(self.screen, subline, term_font, (250, 250, 250),
                            term_header_x, term_header_y + offset)
            offset += 15

    def _transform_coords(self, x: int, y: int) -> tuple[int, int]:
        screen_cx = (self.real_minx + self.real_maxx) / 2
        screen_cy = (self.real_miny + self.real_maxy) / 2
        screen_x = (self.controller_screen.centerx + (x - screen_cx) *
                    self.scale)
        screen_y = (self.controller_screen.centery + (y - screen_cy) *
                    self.scale)
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
            self._relative_node_coords[node] = (nx, ny)
            pygame.draw.circle(self.screen, node_o.color, (nx, ny), 10)

    def _log_moves(self) -> None:
        log = ""
        for drone in self.drones:
            if not drone.path:
                continue
            for i, (node, t) in enumerate(drone.path):
                if i == 0:
                    continue
                prev_n, prev_t = drone.path[i - 1]
                if t == self.sim_t:
                    if node == prev_n:
                        continue
                    log += f"{drone.id}-{node} "
                elif prev_t < self.sim_t < t:
                    connection = prev_n + '-' + node
                    log += f"{drone.id}-{connection} "

        if log:
            self.moves += 1
            self.log_lines.append(log)
            print(log)

    def _get_frac_time(self, dt: float) -> float:
        if not self.paused:
            self.accumulator += dt
            while self.accumulator >= self.step_duration:
                self.accumulator -= self.step_duration
                self.sim_t += 1
                self._log_moves()
        return self.sim_t + (self.accumulator / self.step_duration)

    def _draw_drones(self, frac_t: float) -> None:
        for i, drone in enumerate(self.drones):
            dx, dy = drone.get_pos(frac_t, self.graph)
            sx, sy = self._transform_coords(dx, dy)
            ox, oy = Utils.drone_offset(i, len(self.drones))
            rect = self.drone_img.get_rect(center=(sx + ox, sy + oy))
            self.screen.blit(self.drone_img, rect)

    def run_step(self, events: list[str], dt: float) -> None:
        self._handle_events(events)
        if self.screamer_active:
            self.screen.blit(self.screamer, (0, 0))
        else:
            frac_t = self._get_frac_time(dt)
            self.screen.fill((0, 0, 0))
            self._draw_controller()
            self._draw_dashboard()
            self._draw_graph()
            self._draw_drones(frac_t)
            if self._to_draw_info != ():
                self._draw_info(self._to_draw_info)
