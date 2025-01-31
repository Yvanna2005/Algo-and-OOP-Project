import tkinter as tk
from tkinter import ttk, messagebox
import Dijkstra

class DijkstraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra Path Finder")
        self.root.geometry("800x600")
        
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
        
        self.notebook.add(self.single_path_tab, text='Single Destination')
        self.notebook.add(self.multiple_dest_tab, text='Multiple Destinations')
        self.notebook.add(self.update_graph_tab, text='Update Graph')
        
        # Setup each tab
        self._setup_single_path_tab()
        self._setup_multiple_dest_tab()
        self._setup_update_graph_tab()
        
        # Load the graph
        self.graph = None
        self._load_graph()

    def _load_graph(self):
        try:
            self.graph = Dijkstra.read_file_graph('Graph_Input.txt')
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