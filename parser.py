import sys
from visualizer import Visualizer


class Parser:
    """Parsing class """
    @classmethod
    def validator(cls, map_file: str) -> "Parser":
        if not os.path.isfile(map_file):
            print(f"Error: '{map_file}' does not exist")
            sys.exit(1)
        with open(map_file, 'r') as file:
            

    def __init__(self, map_file: str) -> None:
        
