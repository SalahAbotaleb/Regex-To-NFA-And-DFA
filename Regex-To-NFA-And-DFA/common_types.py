from typing import TypeAlias, Dict, Set, Tuple

NodeId: TypeAlias = str
Action: TypeAlias = str
AdjacencyList: TypeAlias = Dict[NodeId, Dict[Action, Set[NodeId]]]
