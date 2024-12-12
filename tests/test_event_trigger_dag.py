from grafter.event_trigger_dag import EventTriggerGraph


def test_add_event_trigger():
    graph = EventTriggerGraph()
    graph.add_event_trigger("trigger1", "condition", condition="state['value'] > 10")
    assert "trigger1" in graph.graph.nodes
    assert graph.graph.nodes["trigger1"]["trigger_type"] == "condition"
    assert graph.graph.nodes["trigger1"]["condition"] == "state['value'] > 10"


def test_add_event_dependencies():
    graph = EventTriggerGraph()
    graph.add_event_trigger("trigger1", "condition")
    graph.add_event_trigger("trigger2", "condition")
    graph.add_edge("trigger1", "trigger2")
    assert ("trigger1", "trigger2") in graph.graph.edges


def test_evaluate_condition():
    graph = EventTriggerGraph()
    condition = "state['value'] > 10"
    state = {"value": 15}
    assert graph.evaluate_condition(condition, state)
    state = {"value": 5}
    assert not graph.evaluate_condition(condition, state)


def test_check_time_trigger():
    graph = EventTriggerGraph()
    trigger_time = "00:00"
    assert graph.check_time_trigger(trigger_time)
    trigger_time = "23:59"
    assert not graph.check_time_trigger(trigger_time)


def test_check_triggers():
    graph = EventTriggerGraph()
    graph.add_event_trigger("trigger1", "condition", condition="state['value'] > 10")
    state = {"value": 15}
    assert graph.check_triggers(state)
    state = {"value": 5}
    assert not graph.check_triggers(state)


def test_add_data_node():
    graph = EventTriggerGraph()
    graph.add_data_node("data1")
    assert "data1" in graph.graph.nodes
