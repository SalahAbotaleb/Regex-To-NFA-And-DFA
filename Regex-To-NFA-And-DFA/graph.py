from node import Node
from constants import JsonNamings


class Graph:
    def __init__(self, json: dict = None, start_node: Node = None):
        if json is None:
            if start_node is None:
                self.start = Node()
            else:
                self.start = start_node
        else:
            self.__create_from_json__(json)

    def __create_from_json__(self, json: dict):
        '''
        Example for expected input:
        {
            "startingState": "S0",
            "S0": {
                "isTerminatingState": false,
                "A": ["S1"],
                "B": ["S0"]
            },
            "S1": {
                "isTerminatingState": true,
                "A": ["S1"],
                "B": ["S1"]
            }
        }
        '''
        nodes_dict: dict[str, Node] = dict()
        for key, value in json.items():
            if key == JsonNamings.START_STATE:
                node_id = value
                if node_id not in nodes_dict:
                    nodes_dict[node_id] = Node(node_id)
                self.start = nodes_dict[node_id]
                nodes_dict[node_id].is_start = True
            else:
                node_id = key
                if node_id not in nodes_dict:
                    nodes_dict[node_id] = Node(node_id)
                self.__process_inner_json__(
                    nodes_dict[node_id], value, nodes_dict)

    def __process_inner_json__(self, node: Node, json: dict[str, str], nodes_dict: dict[str, Node]):
        for key, value in json.items():
            if key == JsonNamings.TERMINATING_STATE:
                node.is_terminal = value
            else:
                action = key
                nodes_ids = value
                for node_id in nodes_ids:
                    if node_id not in nodes_dict:
                        nodes_dict[node_id] = Node(node_id)
                    node.add_edge(nodes_dict[node_id], action)

    def get_start(self) -> Node:
        return self.start

    def get_terminals(self) -> list[Node]:
        return self.__get_terminals__(self.start, set())

    def __get_terminals__(self, curr_node: Node, visited_nodes: set) -> list[Node]:
        ans = []
        if curr_node.is_terminal == 1:
            ans.append(curr_node)
        visited_nodes.add(curr_node)

        for edge in curr_node.edges:
            neighbor = edge.dest
            if neighbor not in visited_nodes:
                ans.extend(self.__get_terminals__(neighbor, visited_nodes))

        return ans

    def to_json(self):
        json = {"startingState": str(self.start.id)}
        json.update(self.__get_json__(self.start, set()))
        return json

    def __get_json__(self, curr_node: Node, visited_nodes: set) -> dict:
        json = {}
        node_json_key = str(curr_node.id)
        node_json_value = curr_node.to_json()
        json.update({node_json_key: node_json_value})
        visited_nodes.add(curr_node)

        for edge in curr_node.edges:
            neighbor = edge.dest
            if neighbor not in visited_nodes:
                json.update(self.__get_json__(neighbor, visited_nodes))
        return json


if __name__ == "__main__":
    g1 = Graph()
    node1 = g1.get_start()
    node2 = Node()
    node3 = Node()
    node2.is_terminal = 1
    node2.add_edge(node3, "xyz")
    node1.add_edge(node2, "a")
    print(g1.get_start())
    print(g1.get_terminals())
    print(g1.to_json())
    jsonG = g1.to_json()
    g2 = Graph(jsonG)
    print(g2.to_json())
