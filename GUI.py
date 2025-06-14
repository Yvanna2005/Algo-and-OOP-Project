import tkinter as tk
from tkinter import ttk, messagebox
import Dijkstra
import math
import random

class DijkstraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra Path Finder")
        self.root.geometry("1200x800")

        # Main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))

        # Header
        header_label = ttk.Label(
            self.main_frame,
            text="Transportation Network Path Finder",
            style='Header.TLabel'
        )
        header_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create notebook for different operations
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')

        # Create tabs
        self.single_path_tab = ttk.Frame(self.notebook)
        self.multiple_dest_tab = ttk.Frame(self.notebook)
        self.update_graph_tab = ttk.Frame(self.notebook)
        self.graph_view_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.single_path_tab, text='Single Destination')
        self.notebook.add(self.multiple_dest_tab, text='Multiple Destinations')
        self.notebook.add(self.update_graph_tab, text='Update Graph')
        self.notebook.add(self.graph_view_tab, text='Graph View')

        # Setup each tab
        self._setup_single_path_tab()
        self._setup_multiple_dest_tab()
        self._setup_update_graph_tab()
        self._setup_graph_view_tab()

        # Load the graph
        self.graph = None
        self._load_graph()

    def _load_graph(self):
        try:
            self.graph = Dijkstra.read_file_graph('Graph_Input.txt')
            self._update_graph_view()
            messagebox.showinfo("Success", "Graph loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph: {str(e)}")

    def _setup_single_path_tab(self):
        # Single path inputs
        ttk.Label(self.single_path_tab, text="Start Location:").grid(row=0, column=0, pady=5, padx=5)
        self.start_location = ttk.Entry(self.single_path_tab)
        self.start_location.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self.single_path_tab, text="End Location:").grid(row=1, column=0, pady=5, padx=5)
        self.end_location = ttk.Entry(self.single_path_tab)
        self.end_location.grid(row=1, column=1, pady=5, padx=5)

        # Results display
        self.single_path_result = tk.Text(self.single_path_tab, height=10, width=50)
        self.single_path_result.grid(row=3, column=0, columnspan=2, pady=10, padx=5)

        ttk.Button(
            self.single_path_tab,
            text="Find Path",
            command=self._find_single_path
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def _setup_multiple_dest_tab(self):
        ttk.Label(self.multiple_dest_tab, text="Start Location:").grid(row=0, column=0, pady=5, padx=5)
        self.multi_start = ttk.Entry(self.multiple_dest_tab)
        self.multi_start.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self.multiple_dest_tab, text="Destinations\n(space-separated):").grid(row=1, column=0, pady=5, padx=5)
        self.destinations = ttk.Entry(self.multiple_dest_tab)
        self.destinations.grid(row=1, column=1, pady=5, padx=5)

        self.multi_path_result = tk.Text(self.multiple_dest_tab, height=10, width=50)
        self.multi_path_result.grid(row=3, column=0, columnspan=2, pady=10, padx=5)

        ttk.Button(
            self.multiple_dest_tab,
            text="Find Multiple Paths",
            command=self._find_multiple_paths
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def _setup_update_graph_tab(self):
        # Update graph inputs
        ttk.Label(self.update_graph_tab, text="Start Location:").grid(row=0, column=0, pady=5, padx=5)
        self.update_start = ttk.Entry(self.update_graph_tab)
        self.update_start.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self.update_graph_tab, text="End Location:").grid(row=1, column=0, pady=5, padx=5)
        self.update_end = ttk.Entry(self.update_graph_tab)
        self.update_end.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self.update_graph_tab, text="Distance (km):").grid(row=2, column=0, pady=5, padx=5)
        self.distance = ttk.Entry(self.update_graph_tab)
        self.distance.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(self.update_graph_tab, text="Delay Time (hrs):").grid(row=3, column=0, pady=5, padx=5)
        self.delay_time = ttk.Entry(self.update_graph_tab)
        self.delay_time.grid(row=3, column=1, pady=5, padx=5)

        ttk.Button(
            self.update_graph_tab,
            text="Update Graph",
            command=self._update_graph
        ).grid(row=4, column=0, columnspan=2, pady=10)

    def _setup_graph_view_tab(self):
        # Create a frame for the graph view
        graph_frame = ttk.Frame(self.graph_view_tab)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add zoom controls in a more compact way
        zoom_frame = ttk.Frame(graph_frame)
        zoom_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        ttk.Button(zoom_frame, text="+", width=3, command=lambda: self._zoom(1.2)).pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="-", width=3, command=lambda: self._zoom(0.8)).pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="Reset", width=6, command=self._reset_view).pack(side=tk.LEFT, padx=2)

        # Create a frame for canvas and scrollbars
        canvas_frame = ttk.Frame(graph_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Create Canvas widget with larger size
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=1000, height=700)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbars
        vsb = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        hsb = ttk.Scrollbar(graph_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout for scrollbars
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind mouse wheel to canvas scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

        # Initialize variables for node dragging
        self.dragged_node = None
        self.node_positions = {}
        self.edge_items = {}

        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-1>", self._on_node_press)
        self.canvas.bind("<B1-Motion>", self._on_node_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_node_release)

        self.zoom_level = 1.0

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def _zoom(self, factor):
        self.zoom_level *= factor
        self._update_graph_view()

    def _reset_view(self):
        self.zoom_level = 1.0
        self._update_graph_view()

    def _calculate_force_layout(self, num_nodes):
        # Initialize random positions with larger spread
        positions = {}
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Use more of the available space
        margin = 100  # Reduced margin
        for i in range(num_nodes):
            positions[i] = {
                'x': random.uniform(margin, canvas_width - margin),
                'y': random.uniform(margin, canvas_height - margin),
                'vx': 0,
                'vy': 0
            }

        # Force-directed layout parameters adjusted for larger space
        k = 400  # Increased optimal distance between nodes
        iterations = 50
        repulsion = 1500  # Increased repulsion
        attraction = 0.15  # Increased attraction

        for _ in range(iterations):
            # Calculate repulsive forces
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    dx = positions[j]['x'] - positions[i]['x']
                    dy = positions[j]['y'] - positions[i]['y']
                    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)

                    # Repulsive force
                    force = repulsion / (distance * distance)
                    fx = force * dx / distance
                    fy = force * dy / distance

                    positions[i]['vx'] -= fx
                    positions[i]['vy'] -= fy
                    positions[j]['vx'] += fx
                    positions[j]['vy'] += fy

            # Calculate attractive forces for connected nodes
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if i != j and self.graph[i][j][0] != 0:
                        dx = positions[j]['x'] - positions[i]['x']
                        dy = positions[j]['y'] - positions[i]['y']
                        distance = max(math.sqrt(dx*dx + dy*dy), 0.1)

                        # Attractive force
                        force = attraction * (distance - k)
                        fx = force * dx / distance
                        fy = force * dy / distance

                        positions[i]['vx'] += fx
                        positions[i]['vy'] += fy
                        positions[j]['vx'] -= fx
                        positions[j]['vy'] -= fy

            # Update positions
            for i in range(num_nodes):
                positions[i]['x'] += positions[i]['vx'] * 0.1
                positions[i]['y'] += positions[i]['vy'] * 0.1

                # Damping
                positions[i]['vx'] *= 0.9
                positions[i]['vy'] *= 0.9

                # Keep nodes within bounds with smaller margin
                positions[i]['x'] = max(50, min(positions[i]['x'], canvas_width - 50))
                positions[i]['y'] = max(50, min(positions[i]['y'], canvas_height - 50))

        return positions

    def _on_node_press(self, event):
        # Get the clicked position
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        # Find if a node was clicked
        for node_id, (node_x, node_y) in self.node_positions.items():
            if abs(x - node_x) <= 25 and abs(y - node_y) <= 25:  # 25 is the node radius
                self.dragged_node = node_id
                break

    def _on_node_drag(self, event):
        if self.dragged_node is not None:
            # Get the new position
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            # Update node position
            self.node_positions[self.dragged_node] = (x, y)

            # Redraw the graph
            self._redraw_graph()

    def _on_node_release(self, event):
        self.dragged_node = None

    def _redraw_graph(self):
        # Clear existing items
        self.canvas.delete("all")

        # Draw edges first
        for (start_node, end_node), edge_data in self.edge_items.items():
            start_x, start_y = self.node_positions[start_node]
            end_x, end_y = self.node_positions[end_node]

            # Draw the edge
            self.canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill='gray', width=2, arrow=tk.LAST,
                smooth=True
            )

            # Calculate edge angle
            dx = end_x - start_x
            dy = end_y - start_y
            angle = math.atan2(dy, dx)

            # Calculate perpendicular offset for label
            offset = 15
            perp_x = -math.sin(angle) * offset
            perp_y = math.cos(angle) * offset

            # Calculate midpoint for edge label
            mid_x = (start_x + end_x) / 2 + perp_x
            mid_y = (start_y + end_y) / 2 + perp_y

            # Add edge properties
            distance, delay, fuel = edge_data
            label_text = f"D:{distance:.1f}\nT:{delay:.1f}\nF:{fuel:.2f}"

            # Create background rectangle
            text_width = 60
            text_height = 45
            self.canvas.create_rectangle(
                mid_x - text_width/2, mid_y - text_height/2,
                mid_x + text_width/2, mid_y + text_height/2,
                fill='white', outline='gray'
            )

            # Add the text
            self.canvas.create_text(
                mid_x, mid_y,
                text=label_text,
                fill='black',
                font=('Arial', 8),
                justify=tk.CENTER
            )

        # Draw nodes
        for node_id, (x, y) in self.node_positions.items():
            # Draw node circle
            self.canvas.create_oval(
                x-25, y-25, x+25, y+25,
                fill='lightblue',
                outline='blue',
                width=2
            )

            # Add node number
            self.canvas.create_text(
                x, y,
                text=str(node_id),
                fill='black',
                font=('Arial', 12, 'bold')
            )

    def _update_graph_view(self):
        # Clear existing items
        self.canvas.delete("all")
        self.node_positions.clear()
        self.edge_items.clear()

        if not self.graph:
            return

        # Calculate initial node positions using force-directed layout
        initial_positions = self._calculate_force_layout(len(self.graph))

        # Apply zoom level and store positions
        zoom = self.zoom_level
        center_x = self.canvas.winfo_width() / 2
        center_y = self.canvas.winfo_height() / 2

        # Store node positions
        for i in range(len(self.graph)):
            x = center_x + (initial_positions[i]['x'] - center_x) * zoom
            y = center_y + (initial_positions[i]['y'] - center_y) * zoom
            self.node_positions[i] = (x, y)

        # Store edge information
        drawn_edges = set()
        for i in range(len(self.graph)):
            for j in range(len(self.graph)):
                if i != j and self.graph[i][j][0] != 0:
                    edge_key = tuple(sorted([i, j]))
                    if edge_key in drawn_edges:
                        continue

                    if self.graph[i][j][0] <= self.graph[j][i][0]:
                        start_node, end_node = i, j
                    else:
                        start_node, end_node = j, i

                    drawn_edges.add(edge_key)
                    self.edge_items[(start_node, end_node)] = self.graph[start_node][end_node]

        # Draw the graph
        self._redraw_graph()

        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _find_single_path(self):
        try:
            start = int(self.start_location.get())
            end = int(self.end_location.get())

            path, cost = Dijkstra.Dijkstras(self.graph, start, end)

            if path:
                display = " -> ".join(map(str, path))
                result_text = f"Shortest path: {display}\nTotal cost: £{cost:.2f}"
                self.single_path_result.delete(1.0, tk.END)
                self.single_path_result.insert(tk.END, result_text)
            else:
                messagebox.showerror("Error", "No valid path found!")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _find_multiple_paths(self):
        try:
            start = int(self.multi_start.get())
            destinations = list(map(int, self.destinations.get().split()))

            cost, visited_path = Dijkstra.multiple_destinations(self.graph, start, destinations.copy())

            display = " -> ".join(map(str, visited_path))
            result_text = f"Complete path: {display}\nTotal cost: £{cost:.2f}\n\n"
            result_text += "Individual paths between each pair:\n"

            for i in range(len(visited_path)-1):
                path, cost1 = Dijkstra.Dijkstras(self.graph, visited_path[i], visited_path[i+1])
                path_display = " -> ".join(map(str, path))
                result_text += f"({visited_path[i]},{visited_path[i+1]}): {path_display}\n"

            self.multi_path_result.delete(1.0, tk.END)
            self.multi_path_result.insert(tk.END, result_text)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _update_graph(self):
        try:
            start = int(self.update_start.get())
            end = int(self.update_end.get())
            distance = float(self.distance.get())
            delay = float(self.delay_time.get())

            self.graph = Dijkstra.update_graph(self.graph, start, end, distance, delay, 0.05)
            Dijkstra.write_txt_graph(self.graph, 'Graph_Input.txt')

            # Update the graph view
            self._update_graph_view()

            messagebox.showinfo("Success", "Graph updated successfully!")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = DijkstraGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()