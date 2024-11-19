from graph import Graph
from node import Node
from constants import GraphTerm
from common_types import *


class DFAUtils:

    def get_adjacency_list(graph: Graph) -> AdjacencyList:
        '''
            returns adjacency list contains each node with
            all possible actions and all possible adjacent nodes even
            those with epsilon from that action
            is in form of:
            <code>
            {
                Node_Id: {
                    action: { Node_Ids "all possible nodes can be visited even with epsilon move after the action"}
                }
            }
            </code>
        '''
        return DFAUtils.__get_adjacency_list__(graph.get_start(), set())

    def __get_adjacency_list__(node: Node, vis_nodes: set[str]) -> AdjacencyList:
        if node.id in vis_nodes:
            return None

        vis_nodes.add(node.id)
        node_entry = {}
        node_entry[node.id] = dict()

        action_dest_nodes: dict[Action:set[NodeId]
                                ] = node.get_action_and_dest_nodes_dict()

        for action, dest_nodes in action_dest_nodes.items():
            if action not in node_entry[node.id]:
                node_entry[node.id][action] = set()
            adj_nodes = DFAUtils.__get_all_adjacent_nodes_ids__(
                node, action, set())
            node_entry[node.id][action].update(adj_nodes)
            for dest_node in dest_nodes:
                next_res = DFAUtils.__get_adjacency_list__(
                    dest_node, vis_nodes)
                if next_res != None:
                    node_entry.update(next_res)
        return node_entry

    def get_all_adjacent_nodes_ids(node: Node, action: Action) -> set[NodeId]:
        '''
            returns all nodes can be visited from current node using <b>specific action</b>
            and all nodes can be visited using this specific action then <b>epsilon moves</b>
        '''
        return DFAUtils.__get_all_adjacent_nodes_ids__(node, action, set())

    def __get_all_adjacent_nodes_ids__(node: Node, action: str, vis_nodes: set[str]) -> set[str]:
        if node.id in vis_nodes:
            return None

        vis_nodes.add(node.id)
        adj_nodes = set()
        edges = node.get_edges()

        for edge in edges:
            if edge.action == action:
                adj_nodes.add(edge.dest.id)
                next_nodes = DFAUtils.__get_all_adjacent_nodes_ids__(
                    edge.dest, GraphTerm.EPSILON_ACTION, vis_nodes)
                if next_nodes != None:
                    adj_nodes.update(next_nodes)
        return adj_nodes
