from dataclasses import dataclass


@dataclass
class Node:
	"""Blueprint for a node in the graph"""
	name:str
	x: int
	y: int
	connection: "Node" = None
	zone: str = "normal"
	color: str = None
	max_drones: int = 1