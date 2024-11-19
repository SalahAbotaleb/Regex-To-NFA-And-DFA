from graph import Graph
from node import Node
from constants import GraphTerm
from json_utils import JsonUtils
from typing import Dict, Set, TypeAlias
from collections import deque
from draw import Drawer
from common_types import *
from graph_builder import GraphBuilder
from DFA_utils import DFAUtils
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

DFAAdjacencyList: TypeAlias = Dict["DFANode", list[Tuple[Action, "DFANode"]]]


class DFANode(frozenset):
    def __new__(cls, data):
        return super(DFANode, cls).__new__(cls, data)


NFAAdjacencyList: TypeAlias = AdjacencyList
DFAAdjacencyList: TypeAlias = Dict[DFANode, list[tuple[Action, DFANode]]]


class NFAToDFA:
    def __init__(self, graph: Graph):
        self.graph = graph

    def __get_epsilon_closure__(self) -> set[NodeId]:
        return [self.graph.get_start().id, *DFAUtils.get_all_adjacent_nodes_ids(self.graph.get_start(), GraphTerm.EPSILON_ACTION)]

    def __get_dfa_adjacency_list__(self) -> DFAAdjacencyList:
        dfa_nodes: set[DFANode] = set()
        queue: deque[DFANode] = deque()
        adj_list: NFAAdjacencyList = DFAUtils.get_adjacency_list(self.graph)
        init_nodes_ids: set[str] = self.__get_epsilon_closure__()

        init_node = DFANode(init_nodes_ids)
        dfa_nodes: DFAAdjacencyList = dict()
        queue.append(init_node)

        '''
            NFA Adjacency list format
            {
                Node_Name: {
                    action: {all possible nodes can be visited even with epsilon move after the action}
                }
            }
        '''
        while queue:
            curr_dfa_node: DFANode = queue.popleft()
            edges: dict[Action, set[NodeId]] = dict()
            if curr_dfa_node not in dfa_nodes:
                dfa_nodes[curr_dfa_node] = []

            # A DFANode contains multiple Ids for example: 1,5,0,3
            for node_id in curr_dfa_node:
                for action in adj_list[node_id]:
                    if action == GraphTerm.EPSILON_ACTION:
                        continue
                    if action not in edges:
                        edges[action] = set()
                    for adj_node_id in adj_list[node_id][action]:
                        edges[action].add(adj_node_id)

            for action, dest in edges.items():
                dest_dfa_node = DFANode(dest)
                if dest_dfa_node not in dfa_nodes:
                    dfa_nodes[dest_dfa_node] = []
                    queue.append(dest_dfa_node)
                dfa_nodes[curr_dfa_node].append((action, dest_dfa_node))

        return dfa_nodes

    def __is_node_terminal__(self, curr_node: DFANode, nfa_terminals: list[Node]):
        for state in curr_node:
            for nfa_terminal in nfa_terminals:
                if state == nfa_terminal.id:
                    return True
        return False

    def __is_node_start__(self, curr_node: DFANode, nfa_start: Node):
        return True if nfa_start.id in curr_node else False

    def __get_graph_from_dfa_nodes__(self, dfa_nodes: DFAAdjacencyList) -> Graph:
        generated_graph = None
        generated_graph_nodes: dict[DFANode:Node] = dict()
        nfa_start = self.graph.get_start()
        nfa_terminals = self.graph.get_terminals()
        for node, edge_list in dfa_nodes.items():
            if node not in generated_graph_nodes:
                generated_graph_nodes[node] = Node()

            new_node = generated_graph_nodes[node]
            is_start = self.__is_node_start__(node, nfa_start)
            is_terminal = self.__is_node_terminal__(node, nfa_terminals)

            if is_start == True:
                new_node.set_is_start(True)
                generated_graph = Graph(start_node=new_node)

            new_node.set_is_start(is_start)
            new_node.set_is_terminal(is_terminal)

            for action, adj_node in edge_list:
                if adj_node not in generated_graph_nodes:
                    generated_graph_nodes[adj_node] = Node()
                new_node.add_edge(generated_graph_nodes[adj_node], action)
        return generated_graph

    def convert(self) -> Graph:
        nodes = self.__get_dfa_adjacency_list__()
        return self.__get_graph_from_dfa_nodes__(nodes)


if __name__ == "__main__":
    jsonG = JsonUtils.get_dict_from_file("data1.json")
    g = GraphBuilder.fromJson(jsonG)
    nfaConverter = NFAToDFA(g)
    Drawer.save_finite_automaton(nfaConverter.convert())
