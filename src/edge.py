from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    dest: "Node"
    action: str

    def __str__(self):
        return f"action: {self.action} destination: {self.dest}"
