from graph import Graph
from node import Node
from constants import GraphTerm
from json_utils import JsonUtils
from typing import Dict, Set, TypeAlias
from collections import deque
from draw import Drawer
from DFA_utils import DFAUtils
from common_types import *
from graph_builder import GraphBuilder
from NFA_to_DFA import NFAToDFA
'''
1. Divide nodes into two groups one for terminals and other for non-terminals.
2. Get all possible actions. ✔
3. Define a function spilt that takes list of groups
    this function moves through each group
    for each action in actions:
        for each node in the group:
            get adjacent node for this action
            get adjacent node group
    nodes mapped to same group are then added to new set
    if all nodes are mapped to same set this means no spilt happened
    if new sets were generated this means that a group doesn't map to same group
    given a specific action thus a split has happened.
4. Compare function
    this function have a list of groups and pass them to split function as
    long as new groups are generated till no new groups are generated
5. Merge function
    this function takes a list of groups
    if a group contains more than one node this means a merge has to be done
    first check if one of the nodes is start node then keep it and merge other nodes to it.
    if one of the nodes is terminal node then keep it and merge other nodes to it.
    to merge:
        dfs if a node maps to another one in a merged group then
        add edges to this merged group node
        handle other cases
'''
NodeId: TypeAlias = str
Action: TypeAlias = str
GroupId: TypeAlias = str
Group: TypeAlias = tuple[GroupId, list[NodeId]]


class DFAMinimizer():
    graph: Graph
    actions: list[Action]
    adj_list: AdjacencyList
    group_ids_cnt: int

    def __init__(self, graph: Graph):
        self.graph = graph
        self.actions = graph.get_actions()
        self.adj_list = DFAUtils.get_adjacency_list(graph)
        self.group_ids_cnt = 0

    def __get_next_group_id__(self):
        currId = self.group_ids_cnt
        self.group_ids_cnt = self.group_ids_cnt+1
        return currId

    def minimize(self) -> Graph:
        minimized_graph = Graph()
        groups = self.__split_till_no_more__()
        start_node = self.graph.get_start()
        terminal_nodes = [node.id for node in self.graph.get_terminals()]

        nodes_groups = self.__get_nodes_groups__(groups)
        new_nodes: dict[GroupId, Node] = dict()
        for node_id in self.adj_list:
            group_id = nodes_groups[node_id]

            if group_id not in new_nodes:
                new_nodes[group_id] = Node()

            if self.__is_node_start__(node_id, start_node.id):
                new_nodes[group_id].set_is_start(True)
                minimized_graph.set_start(new_nodes[group_id])

            if self.__is_node_terminal__(node_id, terminal_nodes):
                new_nodes[group_id].set_is_terminal(True)

            for action in self.adj_list[node_id]:
                dest_node_id = list(self.adj_list[node_id][action])[0]
                dest_group_id = nodes_groups[dest_node_id]
                if dest_group_id not in new_nodes:
                    new_nodes[dest_group_id] = Node()
                already_created_actions = [
                    edge.action for edge in new_nodes[group_id].get_edges()]
                if action not in already_created_actions:
                    new_nodes[group_id].add_edge(
                        new_nodes[dest_group_id], action)

        return minimized_graph

    def __split_till_no_more__(self) -> list[Group]:
        curr_groups = self.__get_initial_groups__()
        prevLength = len(curr_groups)
        currLength = 0
        while (prevLength != currLength):
            new_groups = self.__split__(curr_groups)
            prevLength = currLength
            currLength = len(new_groups)
            curr_groups = new_groups
        return curr_groups

    def __get_initial_groups__(self) -> list[Group]:
        terminals_group = [node.id for node in self.graph.get_terminals()]
        non_terminals_group = [
            node.id for node in self.graph.get_non_terminals()]
        terminals_group_id = self.__get_next_group_id__()
        non_terminals_group_id = self.__get_next_group_id__()
        return [(terminals_group_id, terminals_group), (non_terminals_group_id, non_terminals_group)]

    def __split__(self, groups: list[Group]) -> list[Group]:
        nodes_groups = self.__get_nodes_groups__(groups)
        for action in self.actions:
            for group_id, nodes_ids in groups:
                groups_nodes_map_to = self.__get_groups_nodes_map_to__(
                    nodes_ids, nodes_groups, action)
                if len(groups_nodes_map_to) > 1:
                    groups.remove((group_id, nodes_ids))
                    for new_group in groups_nodes_map_to.values():
                        # print(new_group)
                        new_group_id = self.__get_next_group_id__()
                        groups.append((new_group_id, new_group))
                    return groups
        return groups

    def __get_nodes_groups__(self, groups: list[Group]) -> dict[NodeId, GroupId]:
        node_dict: Dict[NodeId, GroupId] = dict()
        for group_id, nodes_ids in groups:
            for node_id in nodes_ids:
                node_dict[node_id] = group_id
        return node_dict

    def __get_groups_nodes_map_to__(self, nodes_ids: set[NodeId], nodes_groups: dict[NodeId, GroupId], action: Action) -> dict[GroupId, NodeId]:
        groups_nodes_map_to: Dict[GroupId, list[NodeId]] = dict()
        for node_id in nodes_ids:
            group_maps_to = None
            if action in self.adj_list[node_id]:
                adj_node = list(self.adj_list[node_id][action])[0]
                group_maps_to = nodes_groups[adj_node]
            if group_maps_to not in groups_nodes_map_to:
                groups_nodes_map_to[group_maps_to] = []
            groups_nodes_map_to[group_maps_to].append(node_id)
        return groups_nodes_map_to

    def __is_node_terminal__(self, node_id: NodeId, terminals: list[NodeId]):
        return True if node_id in terminals else False

    def __is_node_start__(self, node_id: NodeId, start: Node):
        return node_id == start


if __name__ == "__main__":
    jsonG = JsonUtils.get_dict_from_file("data1.json")
    g = GraphBuilder.fromJson(jsonG)
    g2 = NFAToDFA(g).convert()
    dfaMinimizer = DFAMinimizer(g2)
    min_g = dfaMinimizer.minimize()
    Drawer().save_finite_automaton(g2, "auto")
    Drawer().save_finite_automaton(min_g, "auto1")
