# Path Finding Transportation Network Project

This project is a Python application for modeling, updating, and analyzing weighted directed graphs using Dijkstra’s algorithm, with both a command-line and a graphical user interface (GUI). It is designed to help users calculate the most economical path(s) in a graph, considering distance, traffic delay, and fuel consumption.

## Features

- **Graph Input/Output:**
  - Graph data is stored in `Graph_Input.txt`.
  - Each edge is described by `distance`, `delay_time`, and `fuel_consumption`.
  - Easily read, update, and write graph data to file.

- **Interactive Graph Update:**
  - Update distance, delay, or fuel consumption for any edge.
  - Changes are saved both in-memory and to the input file.

- **Shortest Path Calculation:**
  - Uses Dijkstra’s algorithm to find the path with the lowest total cost (not just shortest distance).
  - The total cost is a function of distance, delay, and fuel use:
    ```
    cost = fuel_cost + traffic_cost
    fuel_cost = distance * fuel_consumption * fuel_price
    traffic_cost = (0.0082 * delay_time) + (0.052 * delay_time) + (0.0174 * delay_time)
    ```
  - Reports total cost and the path to follow.

- **Multiple Destination Routing:**
  - Computes the most economical order to visit multiple destinations starting from a given node.
  - Greedily selects the nearest next destination using Dijkstra’s algorithm at each step.

- **Graphical User Interface (GUI):**
  - Visualizes the graph using a force-directed layout for readability.
  - Allows interactive zooming, panning, and dragging of nodes.
  - Lets users compute and see shortest paths and update the graph visually.
  - Multiple tabs for single-destination, multiple-destination, update, and view modes.

- **Force-Directed Layout Algorithm:**
  - Automatically arranges nodes for clear visualization using simulated forces (repulsion and attraction).

## Usage

### Command-Line

1. Run `main.py`:
    ```bash
    python main.py
    ```
2. Follow prompts to:
   - Update the graph
   - Find the shortest path between two nodes
   - Find the best path to visit multiple destinations

### GUI

1. Run `GUI.py`:
    ```bash
    python GUI.py
    ```
2. Use the tabs to:
   - Find a single-destination path
   - Find a route through multiple destinations
   - Update the graph visually
   - View and interact with the graph

## File Structure

- `main.py` — CLI entry point for graph analysis and editing.
- `GUI.py` — Graphical interface for visualization and interaction.
- `Dijkstra.py` — Core algorithms and graph utilities:
    - Dijkstra’s algorithm for single and multiple destinations
    - Graph file reading/writing
    - Cost calculation
- `Graph_Input.txt` — The adjacency matrix for the graph.

## Algorithms

### Dijkstra’s Algorithm

Modified to use a custom cost function that combines:
- Distance
- Delay time
- Fuel consumption (and price)

### Force-Directed Layout

Used in the GUI for automatic node positioning:
- Nodes repel each other, edges act as springs.
- Results in a visually balanced graph.

---

## Example

A graph input line (adjacency for one node) in `Graph_Input.txt`:
```
0.0 0.0 0.0 | 2.0 0.5 0.05 | 4.0 0.2 0.05 | ...
```
Means:
- From current node to node 1: 2km, 0.5hr delay, 0.05 fuel/unit
- To node 2: 4km, 0.2hr delay, 0.05 fuel/unit, etc.

---

## Requirements

- Python 3.12
- tkinter (for GUI)

---

## Authors

- [Yvanna2005](https://github.com/Yvanna2005)
- [sims-yann](https://github.com/sims-yann)

---

## License

MIT License (see LICENSE file if present)
