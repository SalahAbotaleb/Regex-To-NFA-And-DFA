class Edge:
    def __init__(self, dest: "Node", action: str):
        self.dest: "Node" = dest
        self.action: str = action
