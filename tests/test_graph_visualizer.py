import json
from graphedexcel.graph_visualizer import (
    merge_configs,
    load_json_config,
    get_graph_default_settings,
    get_node_colors_and_legend,
    visualize_dependency_graph,
)
import networkx as nx


def test_merge_configs():
    default = {"a": 1, "b": {"c": 2}}
    custom = {"b": {"d": 3}, "e": 4}
    merged = merge_configs(default, custom)
    expected = {"a": 1, "b": {"d": 3}, "e": 4}
    assert merged == expected


def test_load_json_config(tmp_path):
    config_data = {"node_size": 50, "width": 0.2}
    config_file = tmp_path / "test_config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    config = load_json_config(config_file)
    assert isinstance(config, dict)
    assert "node_size" in config
    assert config["node_size"] == 50


def test_get_graph_default_settings():
    settings = get_graph_default_settings(100)
    assert settings["node_size"] == 50
    assert settings["with_labels"] is False

    settings = get_graph_default_settings(300)
    assert settings["node_size"] == 30
    assert settings["fig_size"] == (20, 20)

    settings = get_graph_default_settings(600)
    assert settings["node_size"] == 20
    assert settings["fig_size"] == (25, 25)


def test_get_node_colors_and_legend():
    G = nx.DiGraph()
    G.add_node(1, sheet="Sheet1")
    G.add_node(2, sheet="Sheet2")
    G.add_node(3, sheet="Sheet1")

    node_colors, legend_patches = get_node_colors_and_legend(G, "tab20b")
    assert len(node_colors) == 3
    assert len(legend_patches) == 2


def test_visualize_dependency_graph(tmp_path):
    G = nx.DiGraph()
    G.add_node(1, sheet="Sheet1")
    G.add_node(2, sheet="Sheet2")
    G.add_edge(1, 2)

    file_path = tmp_path / "test_graph"
    visualize_dependency_graph(G, str(file_path))

    assert file_path.with_suffix(".png").exists()
