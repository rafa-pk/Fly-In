import sys
import os
from pygame import Color
from typing import Any, Self
from pydantic import BaseModel, Field, ValidationError, model_validator
# from visualizer import Visualizer
from enum import Enum
from graph_classes import ZoneTypes, NodeTypes, Node, Graph


class MapEntries(Enum):
        NB_OF_DRONES = "nb_drones"
        START_HUB = "start_hub"
        HUB = "hub"
        END_HUB = "end_hub"
        CONNECTION = "connection"


class MetadataKeys(Enum):
        COLOR = "color"
        ZONE = "zone"
        MAX_DRONES = "max_drones"
        MAX_LINK_CAPACITY = "max_link_capacity"


class Parser:

    def _open_file(self, map_file: str) -> dict[str, Any]:
        if not os.path.isfile(map_file):
            print(f"Parsing Error: '{map_file}' not valid or not found")
            sys.exit(1)
        settings = {}
        try:
            with open(map_file, 'r') as file:
                for line in file:
                    line = line.split('#', 1)[0].strip()
                    if not line:
                        continue
                    key, value = line.split(':')
                    if MapEntries(key):
                        settings[key] = value
                if next(iter(settings)) != MapEntries.NB_OF_DRONES:
                    raise Exception("'nb_drones' must be the first valid line")
        except Exception as message:
            print(f"Parsing Error: '{map_file}': {message}")
            sys.exit(1)
        return settings

    
    def create_node(key: str, value: str) -> Node:
        try:
            if key not in NodeTypes:
                raise ValueError("Node must be defines as 'start_hub', 'end_hub' or 'hub'")
            type = key
            fields = value.split(' ')
            print(fields)
        except Exception as message:
            print(f"Node creation failed ({message})")
        return Node(name, type, x, y, zone, color, max_drones)

    def create_graph(self, map_file: str) -> "Graph":   # Will orchestrate parsing through private methods and create Graph object, which will be returned
        
        settings: dict[str, Any] = self._open_file(map_file)
        graph: "Graph" = Graph()
        
        try:
            graph.nb_of_drones = int(settings["nb_of_drones"])
            for key, value in settings.items():
                node = create_node(key, value)
                graph.add_node(node)
        except Exception as message:
            print("Parsing Error: Graph creation: {message}")
            sys.exit(1)
        return graph


            
