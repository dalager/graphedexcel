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

    settings = get_graph_default_settings(600)
    assert settings["node_size"] == 20


def test_get_node_colors_and_legend():
    G = nx.DiGraph()
    G.add_node(1, sheet="Sheet1")
    G.add_node(2, sheet="Sheet2")
    G.add_node(3, sheet="Sheet1")

    node_colors, legend_patches = get_node_colors_and_legend(G, "tab20b")
    assert len(node_colors) == 3
    assert len(legend_patches) == 2


def test_visualize_dependency_graph(tmp_path):
    G = create_two_node_graph()

    file_path = tmp_path / "test_graph"
    visualize_dependency_graph(G, str(file_path))

    assert file_path.with_suffix(".png").exists()


def test_provided_config_path(tmp_path):
    G = create_two_node_graph()

    config_data = {"node_size": 50, "width": 0.2, "fig_size": [4, 4]}
    config_file = tmp_path / "test_config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    file_path = tmp_path / "test_graph"
    visualize_dependency_graph(G, str(file_path), config_path=config_file)


def test_invalid_config_path_will_not_break(tmp_path, caplog):
    G = create_two_node_graph()

    file_path = tmp_path / "test_graph"
    visualize_dependency_graph(G, str(file_path), config_path="invalid_path.json")
    assert "Config file not found" in caplog.text
    assert file_path.with_suffix(".png").exists()


def test_invalid_json_in_config_will_not_break(tmp_path, caplog):
    G = nx.DiGraph()
    config_data = {"node_size": 50, "width": 0.2}
    config_file = tmp_path / "test_config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)
    # remove first character from json file
    with open(config_file, "r") as f:
        data = f.read()
    with open(config_file, "w") as f:
        f.write(data[1:])
    file_path = tmp_path / "test_graph"
    visualize_dependency_graph(G, str(file_path), config_path=config_file)
    assert "Invalid JSON format in config file" in caplog.text
    assert file_path.with_suffix(".png").exists()


def test_all_layouts():
    G = create_two_node_graph()

    for layout in ["spring", "kamada_kawai", "circular", "shell", "spectral"]:
        visualize_dependency_graph(G, layout=layout, output_path=layout + "_layout.png")


def test_unknown_layout_will_fallback():
    G = create_two_node_graph()
    visualize_dependency_graph(G, layout="nosuchlayout", output_path="nosuchlayout.png")


def create_two_node_graph():
    G = nx.DiGraph()
    G.add_node(1, sheet="Sheet1")
    G.add_node(2, sheet="Sheet2")
    G.add_edge(1, 2)
    return G
