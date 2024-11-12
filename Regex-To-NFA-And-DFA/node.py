from edge import Edge
from constants import JsonNamings


class Node:

    id_generator = 0

    def __init__(self, id: int = None):
        self.edges = []
        self.is_terminal = 0
        self.is_start = 0
        if id == None:
            self.id = f'S{Node.id_generator}'
            Node.id_generator += 1
        else:
            self.id = id

    def addEdge(self, dest: "Node", action: str):
        self.edges.append(Edge(dest, action))

    def to_json(self):
        json = {}
        json[JsonNamings.TERMINATING_STATE] = bool(self.is_terminal)
        for edge in self.edges:
            if edge.action not in json:
                json[edge.action] = []
                json[edge.action].append(str(edge.dest.id))
            else:
                json[edge.action].append(str(edge.dest.id))
        return json


if __name__ == "__main__":
    node1 = Node()
    node2 = Node()
    node1.addEdge(node2, "a")
    print(node1.to_json())
