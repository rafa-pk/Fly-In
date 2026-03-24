import sys
import pygame
from visualizer import Visualizer
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
        self.settings = None
        self.map_file: str = None
        self.visualizer = Visualizer(self.screen)
        self._run()

    def _event_handler(self) -> None:
        """event handler method for the graphical loop"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == 

    def _starting_menu(self) -> None:
        """method which calls the menu visualizer, stores the map to be used
        and updates status"""
        self.map_file = self.visualizer.maps_menu()
        self.status = "loading"

    def _program_loading(self) -> None:
        """method which calls loading visualizer while doing the parsing and
        algorithmic logic"""
        #self.settings = Parser(self.map_file)
        #self.path = Algo()
        self.state = "update"

    def _update(self) -> None:
        pass

    def _run(self) -> None:
        """main graphical loop which detects hooks and executes program"""
        program_states = {
                    "menu": self._starting_menu,
                    "loading": self._program_loading,
                    "running":self._update(),
                    }
        self.state = "menu"

        while self.running:
            self._event_handler()
            program_states[self.state]()
            pygame.display.flip()

def main() -> None:
    if len(sys.argv) != 1:
        print("Error: Too many arguments.\tUsage: python3 fly-in.py")
        sys.exit(1)
    else:
        FlyIn()

if __name__ == "__main__":
    main()
