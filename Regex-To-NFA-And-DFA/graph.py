from node import Node

class Graph:
    def __init__(self,json:dict = None):
        if json is None:
            self.start = Node()
        else:
            self.__create_from_json__(json)
            
        
    def __create_from_json__(self,json:dict):
        nodes_dict = dict()
        for key, value in json.items():
            if key == "startingState":
                if value not in nodes_dict:
                    nodes_dict[value] = Node()    
                nodes_dict[value].is_start = True
            else:
                if key not in nodes_dict:
                    nodes_dict[key] = Node()  
                self.__process_inner_json__(nodes_dict[key],value)
    
    def __process_inner_json__(self,node:Node,json:dict[str,str],nodes:dict[str,Node]):
        for key, value in json.items():
            if key == "isTerminatingState":
                node.is_terminal = value
            else:
                if key not in nodes:
                    nodes[key] = Node()
                node.addEdge(nodes[key],value)
        
    def get_start(self) -> Node:
        return self.start
    
    def get_terminals(self) -> list[Node]:
       return self.__get_terminals__(self.start,set())
        
    def __get_terminals__(self,curr_node:Node,visited_nodes:set)->list[Node]:
        ans = []
        if curr_node.is_terminal == 1:
            ans.append(curr_node)
        visited_nodes.add(curr_node)
        
        for edge in curr_node.edges:    
            neighbor = edge.dest
            if neighbor not in visited_nodes:
                ans.extend(self.__get_terminals__(neighbor,visited_nodes))
        
        return ans
    
    def to_json(self):
        json = {"startingState":str(self.start.id)}
        json.update(self.__get_json__(self.start,set()))
        return json
    
    def __get_json__(self,curr_node:Node,visited_nodes:set)->dict:
        json = {}
        node_json_key = str(curr_node.id)
        node_json_value = curr_node.to_json()
        json.update({node_json_key:node_json_value})
        visited_nodes.add(curr_node)
        
        for edge in curr_node.edges:    
            neighbor = edge.dest
            if neighbor not in visited_nodes:
                json.update(self.__get_json__(neighbor,visited_nodes))   
        return json

   
if __name__ == "__main__":
    g1 = Graph()
    node1 = g1.get_start()
    node2 = Node()
    node2.is_terminal = 1
    node1.addEdge(node2,"a")
    print(g1.get_start())
    print(g1.get_terminals())
    print(g1.to_json())
    
    