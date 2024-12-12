from datetime import datetime
from typing import Any

import networkx as nx

from grafter.base_graph import BaseGraph


class EventTriggerGraph(BaseGraph):
    def __init__(self):
        super().__init__()
        self.event_triggers = {}

    def add_event_trigger(self, trigger_id: str, trigger_type: str, condition: str = None, interval: str = None):
        self.graph.add_node(trigger_id, trigger_type=trigger_type, condition=condition, interval=interval)

    def evaluate_condition(self, condition: str, state: dict[str, Any]) -> bool:
        # Mark state as local variable
        state = state
        try:
            return eval(condition)
        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False

    def check_time_trigger(self, trigger_time: str) -> bool:
        # Check if current time is greater than trigger time HH:mm
        current_time = datetime.now().time()
        trigger_time = datetime.strptime(trigger_time, "%H:%M").time()
        return current_time >= trigger_time

    def check_triggers(self, state: dict[str, Any]) -> bool:
        for node in nx.topological_sort(self.graph):
            node_data = self.graph.nodes[node]
            trigger_type = node_data.get("trigger_type")
            condition = node_data.get("condition")
            trigger_time = node_data.get("trigger_time")

            if trigger_type == "condition" and condition:
                if not self.evaluate_condition(condition, state):
                    return False
            elif trigger_type == "time" and trigger_time:
                if not self.check_time_trigger(trigger_time):
                    return False

        return True

    def add_data_node(self, node_id: str):
        self.add_node(node_id)
