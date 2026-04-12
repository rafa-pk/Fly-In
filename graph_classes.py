from enum import Enum
from typing import Any, Self
from pydantic import BaseModel, ValidationError, Field, model_validator


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


class NodeTypes(Enum):
    HUB = "hub"
    START = "start_hub"
    END = "end_hub"


class ZoneTypes(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Node(BaseModel):
    name:str = Field(min_length=1)
    type: NodeTypes = Field(min_length=1)
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    zone: ZoneTypes = Field(default=ZoneTypes.NORMAL)
    color: str = None
    max_drones: int = Field(default=None, ge=1)

    @model_validator(mode='after')
    def node_validator(self) -> Self:
        if '-' in self.name:
            raise ValueError("Parsing Error: Zone names cannot contain dashes")
            sys.exit(1)
        if self.color is None:
            return self
        try:
            Color(self.color)
        except ValueError:
            raise ValueError(f"Parsing Error: Map format not supported: "
                             f"{self.color} is not a valid color")
            sys.exit(1)



class Graph(BaseModel):
    
    def __init__(self) -> None:
        self.nb_of_drones: int
        self.nodes: dict[str, Node] = {}
        self.start: Node | None = None
        self.end: Node | None = None
        #adjacent_nodes: dict[str, Any]

    def add_node(self, node: Node) -> None:
        self.nodes[node.name] = node
        if node.type == NodeTypes.START:
            self.start = node
        elif node.type == NodeTypes.END:
            self.end = node