# Graphed Excel

![Python Version](https://img.shields.io/badge/python-3.12.5-blue)

Python script to visualize dependencies between cells in Excel spreadsheets.

Meant as a tool to visualize and understand the complexity of Excel spreadsheets.

Will generate a graph of the dependencies between cells in an Excel spreadsheet. The graph is generated using the `networkx` library and is visualized using `matplotlib`.

## Install

```bash

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python graphbuilder.py <path_to_excel_file>
```

Depending on the size of the spreadsheet you might want to adjust the plot configuration in the code to to make the graph more readable (remove labels, decrease widhts and sizes etc)

## Sample output

```bash
=== Dependency Graph Summary ===
Number of nodes (cells): 16
Number of edges (dependencies): 17

Nodes with the highest degree:
  Sheet1!B5: 4 dependencies
  Sheet1!B12: 3 dependencies
  Sheet1!B17: 3 dependencies
  Sheet1!I21: 3 dependencies
  Sheet1!G22: 3 dependencies
  Sheet1!B22: 3 dependencies
  Sheet1!B28: 3 dependencies
  Sheet1!G19: 2 dependencies
  Sheet1!B35: 2 dependencies
  Sheet3!A2:A11: 2 dependencies
```

## Sample plot

More in `/images` folder.

![Sample graph](images/simplified_1.xlsx5.png)

## Tests

```bash
pytest test_cell_reference_extraction.py
```
