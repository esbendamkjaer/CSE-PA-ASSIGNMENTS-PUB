from typing import Generic, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, data: T):
        self.data = data

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()