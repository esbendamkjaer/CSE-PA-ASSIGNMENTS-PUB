from typing import TypeVar, Generic, Optional

from assignment03.models.graph.edge import Edge
from assignment03.models.graph.node import Node

T = TypeVar('T')


class Graph(Generic[T]):
    def __init__(self, nodes: set[Node[T]] = set(), edges: set[Edge[T]] = set()):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node: Node[T]):
        self.nodes.add(node)

    def add_edge(self, edge: Edge[T]):
        self.edges.add(edge)

    def get_node(self, data: T) -> Optional[Node[T]]:
        for node in self.nodes:
            if node.data == data:
                return node
        return None

    def get_edges(self, node: Node[T]) -> list[Edge[T]]:
        return [edge for edge in self.edges if edge.source == node]
