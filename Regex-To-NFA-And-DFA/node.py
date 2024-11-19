from edge import Edge
from constants import JsonNamings


class Node:

    id_generator = 0

    def __init__(self, id: str = None):
        self.edges: list[Edge] = []
        self.is_terminal = 0
        self.is_start = 0
        if id == None:
            self.id = f'S{Node.id_generator}'
            Node.id_generator += 1
        else:
            self.id = id

    def set_is_start(self, is_start):
        self.is_start = is_start

    def set_is_terminal(self, is_terminal):
        self.is_terminal = is_terminal

    def add_edge(self, dest: "Node", action: str):
        self.edges.append(Edge(dest, action))

    def get_actions(self) -> set[str]:
        actions = set()
        for edge in self.edges:
            actions.add(edge.action)
        return actions

    def get_action_and_dest_nodes_dict(self) -> dict[str:set[str]]:
        '''
        return a dictionary with key of actions and value as set of destination ids
        '''
        actions: dict[str:set[str]] = dict()
        for edge in self.edges:
            if edge.action not in actions:
                actions[edge.action] = set()
            actions[edge.action].add(edge.dest)
        return actions

    def get_edges(self) -> list[Edge]:
        return self.edges

    def remove_edge(self, edge: Edge) -> None:
        self.edges.remove(edge)

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

    def __str__(self) -> str:
        return self.id


if __name__ == "__main__":
    node1 = Node()
    node2 = Node()
    node1.add_edge(node2, "a")
    print(node1.to_json())
    print(node1.get_actions())
