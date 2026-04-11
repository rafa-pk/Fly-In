import sys
import os
from typing import Any
from pydantic import BaseModel, Field
from visualizer import Visualizer
from enum import Enum


class Node(BaseModel):
    name:str
    x: int
    y: int
    connection: "Node" = None
    zone: str = "normal"
    color: str = None
    max_drones: int = 1

class Parser:

    class MapEntries(Enum):
        NB_OF_DRONES = "nb_drones"
        START_HUB = "start_hub"
        HUB = "hub"
        END_HUB = "end_hub"


    class MetadataKeys(Enum):
        COLOR = "color"
        ZONE = "zone"
        MAX_DRONES = "max_drones"
        MAX_LINK_CAPACITY = "max_link_capacity"

    def validator(map_file: str) -> dict[Any]:

    
