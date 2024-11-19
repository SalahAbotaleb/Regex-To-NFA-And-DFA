from graph import Graph
from node import Node
from constants import JsonNamings


class GraphBuilder:
    def fromJson(json: dict) -> Graph:
        return GraphBuilder.__create_from_json__(json)

    def __create_from_json__(json: dict):
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
        graph = Graph()
        nodes_dict: dict[str, Node] = dict()
        for key, value in json.items():
            if key == JsonNamings.START_STATE:
                node_id = value
                if node_id not in nodes_dict:
                    nodes_dict[node_id] = Node(node_id)
                graph.set_start(nodes_dict[node_id])
                nodes_dict[node_id].is_start = True
            else:
                node_id = key
                if node_id not in nodes_dict:
                    nodes_dict[node_id] = Node(node_id)
                GraphBuilder.__process_inner_json__(
                    nodes_dict[node_id], value, nodes_dict)
        return graph

    def __process_inner_json__(node: Node, json: dict[str, str], nodes_dict: dict[str, Node]):
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
