import networkx as nx


class BaseGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: str, **attrs):
        self.graph.add_node(node_id, **attrs)

    def add_edge(self, from_node: str, to_node: str):
        self.graph.add_edge(from_node, to_node)
        if not nx.is_directed_acyclic_graph(self.graph):
            self.graph.remove_edge(from_node, to_node)
            raise ValueError(f"Adding edge from {from_node} to {to_node} would create a cycle.")
