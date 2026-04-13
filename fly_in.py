import sys
import pygame
from file_menu import FileMenu
#from parser import Parser


class FlyIn:
    """Orchestrator class: Bridges gap between program and pygame"""
    def __init__(self) -> None:
        """Initialization method: inits pygame and everything the
        program will need"""
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("Fly In (Visualizer) @ 42Belgium")
        self.running: bool = True
        self.state: str = None
        self.map_file: str = None
        self.file_menu = FileMenu(self.screen, self)
        self._run()

    def status(self, program_status: bool) -> None:
        self.running = program_status

    def _starting_menu(self, events: list[str]) -> None:
        """method which calls the menu visualizer, stores the map to be used
        and updates status"""
        self.map_file = self.file_menu.menu(events)
        if self.map_file is not None:
            print(self.map_file)
            self.screen.fill((0, 0, 0))
            self.state = "loading"

    def _program_loading(self, events: list[str]) -> None:
        """method which calls loading visualizer while doing the parsing and
        algorithmic logic"""
        from parser import Parser
        parser = Parser()
        self.node_graph: Graph = parser.create_graph(self.map_file)
        self.state = "running"

    def _update(self, events: list[str]) -> None:
        # self.algo
        pass

    def _run(self) -> None:
        """main graphical loop which detects hooks and executes program"""
        program_states = {
                    "menu": self._starting_menu,
                    "loading": self._program_loading,
                    "running":self._update,
                    }
        self.state = "menu"

        try:
            while self.running:
                events = pygame.event.get()
                program_states[self.state](events)
                pygame.display.flip()
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit(1)


def main() -> None:
    if len(sys.argv) != 1:
        print("\nError: Too many arguments.\n\tUsage: python3 fly_in.py")
        sys.exit(1)
    else:
        FlyIn()

if __name__ == "__main__":
    main()
