from typing import Generic, TypeVar

from assignment03.models.graph.node import Node

T = TypeVar('T')


class Edge(Generic[T]):
    def __init__(self, source: Node[T], target: Node[T]):
        self.source = source
        self.target = target
        self.relationship = None

    def __hash__(self):
        return hash(
            (self.source, self.target)
        )

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()