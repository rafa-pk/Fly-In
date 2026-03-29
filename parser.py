import sys
from visualizer import Visualizer


class Parser:
    """Parsing class """
    @classmethod
    def validator(cls, map_file: str) -> "Parser":
        if not os.path.isfile(map_file):
            print(f"Error: '{map_file}' does not exist")
            sys.exit(1)
        try:
            with open(map_file, 'r') as file:
                for line in file:
                    line.split(':', 1)[1].strip()
        except Exception as error:
            print("Parsing Error: '{map_file}': {error}")
            sys.exit(1)


    def __init__(self, map_file: str) -> None:
        
