import sys
import pygame
from parser import Parser
from algo_classes import Utils
from algo import FleetPlanner


class FlyIn:
    """Orchestrator class: Bridges gap between program and pygame."""
    def __init__(self) -> None:
        """Initialization method: inits pygame and essential attrs."""
        from file_menu import FileMenu
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 800))
        pygame.display.set_caption("Fly In (Visualizer) @ 42Belgium")
        self.running: bool = True
        self.state: str = ""
        self.map_file: str = ""
        self.file_menu = FileMenu(self.screen, self)
        self._run()

    def status(self, program_status: bool) -> None:
        """Allows for easy stoping of pygame loop."""
        self.running = program_status

    def _starting_menu(self, events: list[pygame.event.Event],
                       dt: float) -> None:
        """
        Calls graphical map menu, stores the map to be used and updates status.

        Parameters:
        events(list[pygame.event.Event]): list of pygame events to be handled
        dt (float): interval between two frames in seconds
        """
        self.map_file = self.file_menu.menu(events)
        if self.map_file:
            self.screen.fill((0, 0, 0))
            self.state = "loading"

    def _program_loading(self, events: list[pygame.event.Event],
                         dt: float) -> None:
        """
        Calls the algorithm and parsing logic and initializes simulation,
        updates state.

        Parameters:
        events(list[pygame.event.Event]): list of pygame events to be handled
        dt (float): interval between two frames in seconds
        """
        from simulation import Simulation
        parser = Parser()
        self.node_graph = parser.create_graph(self.map_file)
        self.drones = Utils.init_drones(self.node_graph)
        planner = FleetPlanner(self.drones, self.node_graph)
        planner.plan_routes()
        self.sim = Simulation(self, self.screen, self.node_graph, self.drones)
        self.state = "running"

    def _update(self, events: list[pygame.event.Event], dt: float) -> None:
        """
        Calls simulation for one discrete step.

        Parameters:
        events(list[pygame.event.Event]): list of pygame events to be handled
        dt (float): interval between two frames in seconds
        """
        self.sim.run_step(events, dt)

    def _run(self) -> None:
        """Main graphical loop which gets events/state and executes program."""
        program_states = {
                    "menu": self._starting_menu,
                    "loading": self._program_loading,
                    "running": self._update,
                    }
        self.state = "menu"
        time = pygame.time.Clock()

        try:
            while self.running:
                dt = time.tick(60) / 1000.0
                events = pygame.event.get()
                program_states[self.state](events, dt)
                pygame.display.flip()
        except KeyboardInterrupt:
            print("Error: Main loop: Program interrupted")
            pygame.quit()
            sys.exit(1)


def main() -> None:
    """Main function, rejects wrong input and instantiates FlyIn object."""
    if len(sys.argv) != 1:
        print("\nError: Too many arguments.\n\tUsage: python3 fly_in.py")
        sys.exit(1)
    # if len((sys.argv) > 2 or
    #        (len(sys.argv) == 2 and sys.argv[1] != "--capacity-info")):
    #    print("\nError: Wrong args")
    #    sys.exit(1)
    else:
        FlyIn()


if __name__ == "__main__":
    """Program's entry point, calls main function."""
    main()
