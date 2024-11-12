# Graphedexcel

[![current release version](https://img.shields.io/github/release/dalager/graphedexcel.svg?style=flat-square)](https://github.com/dalager/graphedexcel/releases)
[![pypi version](https://img.shields.io/pypi/v/graphedexcel.svg?style=flat-square)](https://pypi.python.org/pypi/graphedexcel)
![Python Version](https://img.shields.io/badge/python-3.10%3A3.13-blue?style=flat-square)
[![codecov](https://codecov.io/github/dalager/graphedexcel/branch/main/graph/badge.svg?token=CJM0EAUF9M)](https://codecov.io/github/dalager/graphedexcel)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9620/badge)](https://www.bestpractices.dev/projects/9620)

<img src="docs/images/Book1.xlsx.png" align="right" width="300" alt="Plot from Example Book1.xlsx file">

## Overview

Graphedexcel takes an Excel file and creates a graph data structure with a visual representation.

<br clear="right"/>

## Usage

GraphedExcel can be used in three ways:

1. As a Python CLI tool, installed from PyPi with `pip install graphedexcel` (requires Python)
2. As a Docker container, `ghcr.io/dalager/graphedexcel`, exposing the CLI tool, not requiring any python dependencies being installed. (Requires Docker)
3. As a Python module used within your own code, by importing the `graphedexcel` module. (Requires Python and some python programming experience)

### CLI Tool

```bash
# Install it
pip install graphedexcel
# Run it
python -m graphedexcel <path_to_excel_file>
```

See the command line options below.

### Docker

GraphedExcel is published to <https://ghcr.io/dalager/graphedexcel> and can be run with the following command:

```bash
docker run -v $(pwd):/data ghcr.io/dalager/graphedexcel /data/myworkbook.xlsx -o /data/myworkbook.png
```

Where `myworkbook.xlsx` is sitting in the current directory and the output image will be saved as `myworkbook.png`, also in the current directory.

The `-v` flag is used to mount the current directory into the container as `/data/`

For powershell, use `${pwd}` instead of `$(pwd)` to get the current directory.

### Python Module

```python
import graphedexcel as ge

graph,stats = ge.graphbuilder.build_graph_and_stats("Book1.xlsx")
ge.graph_summarizer.print_summary(graph, stats)
ge.graph_visualizer.visualize_dependency_graph(graph)

```

## Definitions

Single-cell references in a formula sitting in cell `A3` like `=A1+A2` is considered a dependency between the node `A3` and the nodes `A2` and `A1`.

```mermaid
graph TD
    A3 --> A1
    A3 --> A2
    A3["A3=A1+A2"]
```

A range defined in a formula like `=SUM(B1:B3)` is kept as a single node in the graph, but all the containing cells are expanded as dependencies of the range node.

So when a cell, `C1` contains `=SUM(B1:B3)` the graph will look like this:

```mermaid

graph TD
    R --> B1
    R --> B2
    R --> B3
    R["B1:B3"]
    C1 --> R

    C1["C1=SUM(B1:B3)"]

```

## Build and run from source

### Prerequisites

- Python 3.10 or later
- Poetry (<https://python-poetry.org/>)

```bash
poetry install
poetry run graphedexcel <path_to_excel_file> [options]
```

## Using the CLI tool and its varous options

```bash
python -m graphedexcel <path_to_excel_file>
```

### Parameters from `--help`

```
usage: graphedexcel [-h] [--as-directed-graph] [--no-visualize]
                    [--layout {spring,circular,kamada_kawai,shell,spectral}]
                    [--config CONFIG] [--output-path OUTPUT_PATH]
                    [--open-image]
                    path_to_excel

Process an Excel file to build and visualize dependency graphs.

positional arguments:
  path_to_excel         Path to the Excel file to process.

options:
  -h, --help            show this help message and exit
  --as-directed-graph, -d
                        Treat the dependency graph as directed.
  --no-visualize, -n    Skip the visualization of the dependency
                        graph.
  --layout, -l {spring,circular,kamada_kawai,shell,spectral}
                        Layout algorithm for graph visualization
                        (default: spring).
  --config, -c CONFIG   Path to the configuration file for
                        visualization. See README for details.
  --output-path, -o OUTPUT_PATH
                        Specify the output path for the generated
                        graph image.
  --open-image          Open the generated image after visualization.
  --hide-legends        Do not show legends in the visualization. (Default: False)
```

## Sample output

The following is the output of running the script on the sample `docs/Book1.xlsx` file.

```bash
===  Dependency Graph Summary ===
Cell/Node count                70
Dependency count              100


===  Most connected nodes     ===
Range Madness!A2:A11           22
Range Madness!B2:B11           11
Range Madness!F1               10
Main Sheet!B5                   4
Main Sheet!B22                  4
Detached !A2:A4                 4
Range Madness!B2                4
Range Madness!B3                4
Range Madness!B4                4
Range Madness!B5                4

===  Most used functions      ===
SUM                             4
POWER                           1

Visualizing the graph of dependencies.
This might take a while...

Graph visualization saved to images/.\Book1.xlsx.png
```

## Sample plot

More in `docs/images` folder.

![Sample graph](docs/images/simplified_1.xlsx5.png)

## Customizing Graph Visualization Settings

You can customize the graph visualization settings by passing a path to a JSON configuration file. This allows you to override the default settings with your own preferences.

Look at <https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html> for the available settings.

### Default Settings

The default settings for the graph visualization in the various sizes (from `graph_visualizer.py`):

```python
# Default settings for the graph visualization
base_graph_settings = {
    "node_size": 50,        # the size of the node
    "width": 0.2,           # the width of the edge between nodes
    "edge_color": "black",  # the color of the edge between nodes
    "linewidths": 0,        # the stroke width of the node border
    "with_labels": False,   # whether to show the node labels
    "font_size": 10,        # the size of the node labels
    "cmap": "tab20b",       # the color map to use for coloring nodes
    "fig_size": (10, 10),   # the size of the figure
}

# Sized-based settings for small, medium, and large graphs
small_graph_settings = {
    "with_labels": False,
    "alpha": 0.8}

medium_graph_settings = {
    "node_size": 30,
    "with_labels": False,
    "alpha": 0.4,
    "fig_size": (20, 20),
}

large_graph_settings = {
    "node_size": 20,
    "with_labels": False,
    "alpha": 0.2,
    "fig_size": (25, 25),
}

```

### Custom JSON Configuration

To override these settings, create a JSON file (e.g., graph_settings.json) with the desired settings. Here is an example of a JSON configuration file:

```json
{
  "node_size": 40,
  "edge_color": "blue",
  "with_labels": true,
  "font_size": 12,
  "alpha": 0.6
}
```

### Using the Custom Configuration

To use the custom configuration, pass the path to the JSON file as an argument to the script:

```bash
python -m graphedexcel myexcel.xlsx --config graph_settings.json
```

This will render the graph using the custom settings defined in the JSON file.

## Tests

Just run pytest in the root folder.

```bash
poetry run pytest
```

### Bandit Security Tests

To run the Bandit (<https://github.com/PyCQA/bandit>) security tests, you can use the following command.
It will report on medium and high severity safety issues.

```bash
poetry run bandit -c pyproject.toml -r . -lll
```
