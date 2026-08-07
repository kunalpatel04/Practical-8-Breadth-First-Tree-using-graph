import heapq
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# PART 1: AVL TREE LOGIC
# ==========================================
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def insert(self, root, key, logs):
        if not root:
            logs.append(f"Inserted node {key}")
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key, logs)
        else:
            root.right = self.insert(root.right, key, logs)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Heavy
        if balance > 1 and key < root.left.key:
            logs.append(f"Right Rotation on node {root.key}")
            return self.right_rotate(root)
        # Right Heavy
        if balance < -1 and key > root.right.key:
            logs.append(f"Left Rotation on node {root.key}")
            return self.left_rotate(root)
        # Left-Right Case
        if balance > 1 and key > root.left.key:
            logs.append(f"Left-Right Rotation on node {root.key}")
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # Right-Left Case
        if balance < -1 and key < root.right.key:
            logs.append(f"Right-Left Rotation on node {root.key}")
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        return root.height if root else 0

    def get_balance(self, root):
        return self.get_height(root.left) - self.get_height(root.right) if root else 0

    def get_pre_order(self, root, result=None):
        if result is None:
            result = []
        if root:
            result.append(str(root.key))
            self.get_pre_order(root.left, result)
            self.get_pre_order(root.right, result)
        return result

# ==========================================
# PART 2: GUI APPLICATION
# ==========================================
class DataStructuresGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Structures Lab: AVL, Heaps & Priority Queue")
        self.root.geometry("650x500")

        # Create Notebook (Tabbed Layout)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: AVL Tree
        self.tab_avl = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_avl, text="AVL Tree")
        self.setup_avl_tab()

        # Tab 2: Min & Max Heap
        self.tab_heap = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_heap, text="Min & Max Heap")
        self.setup_heap_tab()

        # Tab 3: Task Manager (Priority Queue)
        self.tab_task = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_task, text="Task Manager")
        self.setup_task_tab()

    # --- TAB 1: AVL TREE GUI ---
    def setup_avl_tab(self):
        self.avl_tree = AVLTree()
        self.avl_root = None

        frame = ttk.LabelFrame(self.tab_avl, text="AVL Tree Operations", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Insert Value:").grid(row=0, column=0, sticky="w", pady=5)
        self.avl_entry = ttk.Entry(frame, width=15)
        self.avl_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Button(frame, text="Insert Node", command=self.insert_avl).grid(row=0, column=2, pady=5, padx=5)
        ttk.Button(frame, text="Reset Tree", command=self.reset_avl).grid(row=0, column=3, pady=5, padx=5)

        self.avl_output = tk.Text(frame, height=15, width=65, font=("Consolas", 10))
        self.avl_output.grid(row=1, column=0, columnspan=4, pady=10)

        # Pre-load initial values
        initial_values = [10, 20, 30, 40, 50, 25]
        logs = []
        for val in initial_values:
            self.avl_root = self.avl_tree.insert(self.avl_root, val, logs)
        
        self.avl_output.insert(tk.END, f"Initialized AVL with: {initial_values}\n")
        for log in logs:
            self.avl_output.insert(tk.END, f"- {log}\n")
        self.avl_output.insert(tk.END, f"\nPre-Order Traversal: {' -> '.join(self.avl_tree.get_pre_order(self.avl_root))}\n")

    def insert_avl(self):
        try:
            val = int(self.avl_entry.get())
            logs = []
            self.avl_root = self.avl_tree.insert(self.avl_root, val, logs)
            self.avl_entry.delete(0, tk.END)

            self.avl_output.insert(tk.END, f"\n--- Inserted {val} ---\n")
            for log in logs:
                self.avl_output.insert(tk.END, f"- {log}\n")
            self.avl_output.insert(tk.END, f"Current Pre-Order: {' -> '.join(self.avl_tree.get_pre_order(self.avl_root))}\n")
            self.avl_output.see(tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def reset_avl(self):
        self.avl_root = None
        self.avl_output.delete("1.0", tk.END)
        self.avl_output.insert(tk.END, "AVL Tree reset.\n")

    # --- TAB 2: MIN/MAX HEAP GUI ---
    def setup_heap_tab(self):
        frame = ttk.LabelFrame(self.tab_heap, text="Heap Construction", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Comma-separated numbers:").pack(anchor="w", pady=2)
        self.heap_entry = ttk.Entry(frame, width=50)
        self.heap_entry.pack(anchor="w", pady=5)
        self.heap_entry.insert(0, "12, 3, 17, 8, 1, 9")

        ttk.Button(frame, text="Generate Heaps", command=self.build_heaps).pack(anchor="w", pady=5)

        self.heap_output = tk.Text(frame, height=12, width=65, font=("Consolas", 10))
        self.heap_output.pack(pady=10)
        self.build_heaps()

    def build_heaps(self):
        try:
            raw = self.heap_entry.get()
            data = [int(x.strip()) for x in raw.split(",") if x.strip()]
            
            # Min Heap
            min_heap = data.copy()
            heapq.heapify(min_heap)

            # Max Heap
            max_heap = [-x for x in data]
            heapq.heapify(max_heap)
            max_heap_res = [-x for x in max_heap]

            self.heap_output.delete("1.0", tk.END)
            self.heap_output.insert(tk.END, f"Original Data: {data}\n\n")
            self.heap_output.insert(tk.END, f"Min-Heap Array: {min_heap}\n")
            self.heap_output.insert(tk.END, f"Max-Heap Array: {max_heap_res}\n")
        except ValueError:
            messagebox.showerror("Error", "Enter valid integers separated by commas.")

    # --- TAB 3: TASK MANAGER GUI ---
    def setup_task_tab(self):
        self.pq = []

        frame = ttk.LabelFrame(self.tab_task, text="Priority Queue Manager", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="Priority (Integer):").grid(row=0, column=0, padx=5)
        self.prio_entry = ttk.Entry(input_frame, width=8)
        self.prio_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Task:").grid(row=0, column=2, padx=5)
        self.task_entry = ttk.Entry(input_frame, width=30)
        self.task_entry.grid(row=0, column=3, padx=5)

        ttk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=0, column=4, padx=5)

        ttk.Button(frame, text="Process Next Highest Priority Task", command=self.process_task).pack(anchor="w", pady=5)

        self.task_output = tk.Text(frame, height=12, width=65, font=("Consolas", 10))
        self.task_output.pack(pady=5)

        # Pre-load tasks
        initial_tasks = [
            (1, "Critical: Fix server outage"),
            (2, "Medium: Review pull requests"),
            (3, "Low: Update documentation")
        ]
        for priority, desc in initial_tasks:
            heapq.heappush(self.pq, (priority, desc))
        
        self.update_task_display()

    def add_task(self):
        try:
            priority = int(self.prio_entry.get())
            desc = self.task_entry.get().strip()
            if not desc:
                messagebox.showwarning("Warning", "Task description cannot be empty.")
                return

            heapq.heappush(self.pq, (priority, desc))
            self.prio_entry.delete(0, tk.END)
            self.task_entry.delete(0, tk.END)
            self.update_task_display()
        except ValueError:
            messagebox.showerror("Error", "Priority must be an integer (1 = Highest).")

    def process_task(self):
        if not self.pq:
            messagebox.showinfo("Info", "No tasks left to process.")
            return

        priority, task = heapq.heappop(self.pq)
        messagebox.showinfo("Task Processed", f"Processed Task:\n[Priority {priority}] -> {task}")
        self.update_task_display()

    def update_task_display(self):
        self.task_output.delete("1.0", tk.END)
        self.task_output.insert(tk.END, "Current Queue Status (Sorted by Priority):\n")
        self.task_output.insert(tk.END, "-" * 50 + "\n")
        sorted_pq = sorted(self.pq)
        for priority, desc in sorted_pq:
            self.task_output.insert(tk.END, f"Priority {priority} -> {desc}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataStructuresGUI(root)
    root.mainloop()
