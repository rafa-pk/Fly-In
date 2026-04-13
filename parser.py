import sys
import os
from enum import Enum
from typing import Any, Self
from pydantic import BaseModel, Field, ValidationError, model_validator
from graph_classes import MapEntries, ZoneTypes, NodeTypes, MetadataKeys, Node, Edge, Graph


class Parser:

    def _open_file(self, map_file: str) -> dict[str, Any]:
        if not os.path.isfile(map_file):
            print(f"Parsing Error: '{map_file}' not valid or not found")
            sys.exit(1)
        settings = []
        try:
            with open(map_file, 'r') as file:
                for line in file:
                    line = line.split('#', 1)[0].strip()
                    if not line:
                        continue
                    key, value = line.split(':', 1)
                    key = key.strip()
                    if MapEntries(key):
                        settings.append((key, value))
                if settings[0][0] != MapEntries.NB_DRONES.value:
                    raise Exception("'nb_drones' must be the first valid line")
        except Exception as message:
            print(f"Parsing Error: '{map_file}': {message}")
            sys.exit(1)
        return settings

    def _create_node(self, key: str, value: str) -> Node:
        try:
            if not NodeTypes(key):
                raise ValueError("Node must be defined as 'start_hub', 'end_hub' or 'hub'")

            fields = value.split()
            node_data = {
                "name": fields[0],
                 "type": key,   
                 "x": int(fields[1]),
                 "y": int(fields[2]),
            }

            metadata = [field.strip('[]') for field in fields[3:]]
            for data in metadata:
                meta_key, meta_val = data.split('=')
                match MetadataKeys(meta_key):
                    case MetadataKeys.COLOR:
                        node_data["color"] = meta_val
                    case MetadataKeys.ZONE:
                        node_data["zone"] = meta_val
                    case MetadataKeys.MAX_DRONES:
                        node_data["max_drones"] = meta_val
                    case _:
                        raise ValueError("Field 'name' not accepted as node metadata")
        except Exception as message:
            print(f"Parsing Error: Node creation failed ({message})")
            sys.exit(1)
        return Node(**node_data)

    def _create_edge(self, key: str, value: str, graph: Graph) -> Edge:
        edge_data = {}

        try:
            if MapEntries(key) != MapEntries.CONNECTION:
                raise ValueError("'connection' field not properly formatted")
            fields = value.split()
            node1, node2 = fields[0].split('-', 1)
            edge_data["connection"] = (node1, node2)
            edge_data["cost"] = graph.nodes[node1].euclidean_distance_to(graph.nodes[node2])
            if len(fields) > 1:
                meta_key, meta_value = fields[1].strip('[]').split('=', 1)    
                if MetadataKeys(meta_key) == MetadataKeys.MAX_LINK_CAPACITY:
                    edge_data["max_link_capacity"] = meta_value
        except Exception as message:
            print(f"Parsing Error: Edge creation failed ({message})")
            sys.exit(1)
        return Edge(**edge_data)

    def create_graph(self, map_file: str) -> Graph:

        settings: list[tup(str, str)] = self._open_file(map_file)
        graph: "Graph" = Graph()

        try:
            graph.nb_of_drones = int(settings[0][1])
            for key, value in settings[1:]:
                if key in [k.value for k in NodeTypes]: 
                    node = self._create_node(key, value)
                    graph.add_node(node)
                elif key == MapEntries.CONNECTION.value:
                    edge = self._create_edge(key, value, graph)
                    graph.add_edge(edge)
            graph.validate()
        except Exception as message:
            print(f"Parsing Error: Graph creation: {message}")
            sys.exit(1)
        return graph
