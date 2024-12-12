from collections.abc import Callable
from datetime import datetime
from typing import Any

import networkx as nx

from grafter.base_graph import BaseGraph


class FeatureGraph(BaseGraph):
    def __init__(self):
        super().__init__()

    def add_node(self, node_id: str, compute_func: Callable = None):
        self.graph.add_node(node_id, compute_func=compute_func)

    def compute_features(self, state: dict[str, Any]) -> dict[str, Any]:
        features = state
        for node in nx.topological_sort(self.graph):
            compute_func = self.graph.nodes[node]["compute_func"]
            if compute_func is None:
                features[node] = features.get(node)
            else:
                features[node] = compute_func(features)

        result = {"timestamp": datetime.now().timestamp(), "features": features}
        return result

    def add_data_node(self, node_id: str):
        self.add_node(node_id)
