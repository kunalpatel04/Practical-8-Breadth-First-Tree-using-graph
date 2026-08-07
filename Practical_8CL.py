import heapq

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def insert(self, root, key):
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        
        if balance < -1 and key < root.right.key:
            root.right = self.left_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        print(f"Left Rotation on {z.key}")
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        print(f"Right Rotation on {z.key}")
        return y

    def get_height(self, root):
        return root.height if root else 0

    def get_balance(self, root):
        return self.get_height(root.left) - self.get_height(root.right) if root else 0

    def pre_order(self, root):
        if root:
            print(f"{root.key} ", end="")
            self.pre_order(root.left)
            self.pre_order(root.right)

def min_heap_example(data):
    heapq.heapify(data)
    print("Min-Heap:", data)

def max_heap_example(data):
    max_heap = [-elem for elem in data]
    heapq.heapify(max_heap)
    print("Max-Heap:", [-elem for elem in max_heap])

class TaskManager:
    def __init__(self):
        self.pq = []  
    def add_task(self, priority, description):
        heapq.heappush(self.pq, (priority, description))

    def run_tasks(self):
        print("\nProcessing Tasks by Priority:")
        while self.pq:
            priority, task = heapq.heappop(self.pq)
            print(f"Priority {priority} -> Task: {task}")

if __name__ == "__main__":
    print("=== AVL Tree Insertion and Balancing ===")
    avl = AVLTree()
    root = None
    
    avl_inputs = [10, 20, 30, 40, 50, 25]  
    
    for value in avl_inputs:
        print(f"Inserting {value}...")
        root = avl.insert(root, value)

    print("\nAVL Tree Pre-Order Traversal:")
    avl.pre_order(root)

    print("\n\n=== Heap Examples ===")
    
    data = [12, 3, 17, 8, 1, 9]  

    min_heap_example(data.copy())
    max_heap_example(data.copy())

    print("\n\n=== Task Manager using Priority Queue ===")
    manager = TaskManager()
    
    manager.add_task(1, "Critical: Fix server outage")
    manager.add_task(2, "Medium: Review pull requests")
    manager.add_task(3, "Low: Update documentation")

    manager.run_tasks()
