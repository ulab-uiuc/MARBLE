```python
class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def pre_order_helper(self, node):
        if node != TNULL:
            print(node.key)
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    def in_order_helper(self, node):
        if node != TNULL:
            self.in_order_helper(node.left)
            print(node.key)
            self.in_order_helper(node.right)

    def post_order_helper(self, node):
        if node != TNULL:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            print(node.key)

    def search_tree_helper(self, node, key):
        if node == TNULL or key == node.key:
            return node

        if key < node.key:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def fix_delete(self, x):
        # code omitted for brevity

    def rb_transplant(self, u, v):
        # code omitted for brevity

    def delete_node_helper(self, node, key):
        # code omitted for brevity

    def fix_insert(self, k):
        # code omitted for brevity

    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.left = TNULL
        node.right = TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def get_root(self):
        return self.root

    def delete_node(self, data):
        self.delete_node_helper(self.root, data)

    def print_tree(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    def search_tree(self, k):
        return self.search_tree_helper(self.root, k)
```