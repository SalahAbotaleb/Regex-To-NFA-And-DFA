from node import Node
from common_types import *


class Graph:
    def __init__(self, start_node: Node = None):
        if start_node is None:
            self.start = Node()
        else:
            self.start = start_node
        self.local_start_id = 0

    def set_start(self, start_node: Node):
        self.start = start_node

    def get_start(self) -> Node:
        return self.start

    def get_non_terminals(self) -> list[Node]:
        return self.__get_non_terminals__(self.start, set())

    def __get_non_terminals__(self, curr_node: Node, visited_nodes: set) -> list[Node]:
        ans = []
        if curr_node.is_terminal == False:
            ans.append(curr_node)
        visited_nodes.add(curr_node)

        for edge in curr_node.edges:
            neighbor = edge.dest
            if neighbor not in visited_nodes:
                ans.extend(self.__get_non_terminals__(neighbor, visited_nodes))

        return ans

    def get_terminals(self) -> list[Node]:
        return self.__get_terminals__(self.start, set())

    def __get_terminals__(self, curr_node: Node, visited_nodes: set) -> list[Node]:
        ans = []
        if curr_node.is_terminal == True:
            ans.append(curr_node)
        visited_nodes.add(curr_node)

        for edge in curr_node.edges:
            neighbor = edge.dest
            if neighbor not in visited_nodes:
                ans.extend(self.__get_terminals__(neighbor, visited_nodes))

        return ans

    def get_actions(self) -> list[Action]:
        return self.__get_actions__(self.start, set())

    def __get_actions__(self, curr_node: Node, visited_nodes: set) -> set[Action]:
        ans = set()
        visited_nodes.add(curr_node)

        for edge in curr_node.edges:
            neighbor = edge.dest
            ans.add(edge.action)
            if neighbor not in visited_nodes:
                ans.update(self.__get_actions__(neighbor, visited_nodes))

        return ans

    def rename_nodes_ids(self):
        '''Renames graph nodes ids to start from start_id and end at nodes_cnt'''
        new_ids = dict()
        self.__get_new_nodes_ids__(self.get_start(), new_ids)
        for _, node_item in new_ids.items():
            node, new_id = node_item
            node.id = new_id

    def __get_new_nodes_ids__(self, curr_node: Node, visited_nodes: Dict[NodeId, Tuple[Node, NodeId]]):
        if curr_node in visited_nodes:
            return
        visited_nodes[curr_node.id] = (curr_node, self.local_start_id)
        self.local_start_id = self.local_start_id+1
        for edge in curr_node.get_edges():
            neighbor = edge.dest
            self.__get_new_nodes_ids__(neighbor, visited_nodes)


if __name__ == "__main__":
    g1 = Graph()
    node1 = g1.get_start()
    node2 = Node()
    node3 = Node()
    node2.is_terminal = 1
    node2.add_edge(node3, "xyz")
    node1.add_edge(node2, "a")
    g1.rename_nodes_ids()
    # print(g1.get_start())
    # print(g1.get_terminals())
    # print(g1.to_json())
    # jsonG = g1.to_json()
    # g2 = Graph(jsonG)
    # print(g2.to_json())
    # print(g2.get_actions())
