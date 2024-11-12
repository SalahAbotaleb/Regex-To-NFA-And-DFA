from graph import Graph
from node import Node
from constants import GraphTerm
from json_utils import JsonUtils
from typing import Dict, Set, TypeAlias
from collections import deque
from draw import Drawer

'''
Basic idea:

1. Function to get all subsequent nodes if we take action x
   - Where all subsequent nodes which can be reached with the action
        and epsilon moves after the action
2. construct a dict with nodeId: {action:[all result nodes]}
    example: 2 ==action A==> 2,3,5,6,8
3. get epsilon closure:
        all nodes that can be reached with epsilon move
4. for current node (initially epsilon closure)
    dict1 for: action => set(result Nodes)
    for each key in the combinedKey (example: 2,3,5,6,8)
        for each action => add the neighbor nodes to the dict1

    for each action in dict1
        now for each set(result Nodes) check if this node wasn't created before create it
        example dict => set(result Nodes):Node
        then add edge from current node to new  Node created with the action

    add new created nodes to queue then process till no more nodes in the queue
'''


class DFANode(frozenset):
    def __new__(cls, data):
        return super(DFANode, cls).__new__(cls, data)


AdjacencyList: TypeAlias = Dict[str, Dict[str, Set[str]]]
DFANodes: TypeAlias = Dict[DFANode, list[tuple[str, DFANode]]]


class NFAToDFA:
    def __init__(self, graph: Graph):
        self.graph = graph

    def __get_all_adjacent_nodes_ids__(self, node: Node, action: str, vis_nodes: set[str]) -> set[str]:
        if node.id in vis_nodes:
            return None

        vis_nodes.add(node.id)
        adj_nodes = set()
        edges = node.get_edges()

        for edge in edges:
            if edge.action == action:
                adj_nodes.add(edge.dest.id)
                next_nodes = self.__get_all_adjacent_nodes_ids__(
                    edge.dest, GraphTerm.EPSILON_ACTION, vis_nodes)
                if next_nodes != None:
                    adj_nodes.update(next_nodes)
        return adj_nodes

    def __get_adjacency_list__(self, node: Node, vis_nodes: set[str]) -> AdjacencyList:
        '''
            returns adjacency list is in form of:
            {
                Node_Name: {
                    action: {all possible nodes can be visited even with epsilon move after the action}
                }
            }
        '''
        if node.id in vis_nodes:
            return None

        vis_nodes.add(node.id)
        node_entry = {}
        node_entry[node.id] = dict()

        action_dest_nodes: dict[str:set[str]
                                ] = node.get_action_and_dest_nodes_dict()

        for action, dest_nodes in action_dest_nodes.items():
            if action not in node_entry[node.id]:
                node_entry[node.id][action] = set()
            adj_nodes = self.__get_all_adjacent_nodes_ids__(
                node, action, set())
            node_entry[node.id][action].update(adj_nodes)
            for dest_node in dest_nodes:
                next_res = self.__get_adjacency_list__(dest_node, vis_nodes)
                if next_res != None:
                    node_entry.update(next_res)
        return node_entry

    def __get_epsilon_closure__(self) -> set[str]:
        return [self.graph.get_start().id, *self.__get_all_adjacent_nodes_ids__(self.graph.get_start(), GraphTerm.EPSILON_ACTION, set())]

    def __get_dfa_nodes__(self) -> DFANodes:
        nodes: set[DFANode] = set()
        queue: deque[DFANode] = deque()
        adj_list: AdjacencyList = self.__get_adjacency_list__(
            self.graph.get_start(), set())
        init_node_ids: set[str] = self.__get_epsilon_closure__()

        init_node = DFANode(init_node_ids)
        nodes: dict[DFANode:list[DFANode]] = dict()
        queue.append(init_node)

        '''
            Adjacency list format
            {
                Node_Name: {
                    action: {all possible nodes can be visited even with epsilon move after the action}
                }
            }
        '''
        while queue:
            curr_node: DFANode = queue.popleft()
            edges: dict[str, set[str]] = dict()
            if curr_node not in nodes:
                nodes[curr_node] = []

            for state in curr_node:
                for action in adj_list[state]:
                    if action == GraphTerm.EPSILON_ACTION:
                        continue
                    if action not in edges:
                        edges[action] = set()
                    for adj_state in adj_list[state][action]:
                        edges[action].add(adj_state)

            for action, dest in edges.items():
                dest_dfa_node = DFANode(dest)
                if dest_dfa_node not in nodes:
                    nodes[dest_dfa_node] = []
                    queue.append(dest_dfa_node)
                nodes[curr_node].append((action, dest_dfa_node))

        return nodes

    def __is_node_terminal__(self, curr_node: DFANode, nfa_terminals: list[Node]):
        for state in curr_node:
            for nfa_terminal in nfa_terminals:
                if state == nfa_terminal.id:
                    return True
        return False

    def __is_node_start__(self, curr_node: DFANode, nfa_start: Node):
        return True if nfa_start.id in curr_node else False

# DFANodes: TypeAlias = Dict[DFANode:list[tuple(str, DFANode)]]
    def __get_graph_from_dfa_nodes__(self, dfa_nodes: DFANodes) -> Graph:
        generated_graph = None
        generated_graph_nodes: dict[DFANode:Node] = dict()
        nfa_start = self.graph.get_start()
        nfa_terminals = self.graph.get_terminals()
        for node, adj_list in dfa_nodes.items():
            if node not in generated_graph_nodes:
                generated_graph_nodes[node] = Node()

            new_node = generated_graph_nodes[node]
            is_start = self.__is_node_start__(node, nfa_start)
            is_terminal = self.__is_node_terminal__(node, nfa_terminals)

            if is_start == True:
                generated_graph = Graph(start_node=new_node)

            new_node.set_is_start(is_start)
            new_node.set_is_terminal(is_terminal)

            for action, adj_node in adj_list:
                if adj_node not in generated_graph_nodes:
                    generated_graph_nodes[adj_node] = Node()
                new_node.add_edge(generated_graph_nodes[adj_node], action)
        return generated_graph


if __name__ == "__main__":
    jsonG = JsonUtils.get_dict_from_file("data1.json")
    g = Graph(jsonG)
    nfaConverter = NFAToDFA(g)
    adj = nfaConverter.__get_adjacency_list__(
        g.get_start(), set())
    nodes = nfaConverter.__get_dfa_nodes__()
    print(nodes)
    g3 = nfaConverter.__get_graph_from_dfa_nodes__(nodes)
    print(g3)
    Drawer.save_finite_automaton(g3)
