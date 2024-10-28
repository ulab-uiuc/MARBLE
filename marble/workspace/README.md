# README.md

## Overview

A Red-Black Tree is a binary search tree with an additional bit of data for balancing. The python implementation of Red-Black Tree includes methods for insertion, deletion, search, and traversal. The Red-Black Tree maintains all properties such as every node having a color either red or black, the root of the tree is always black, all leaves (NULL) are black, if a node is red, then both its children are black, and every simple path from a node to its descendant leaves contains an equal number of black nodes.

## Class & Method Summary

#### Class `Node`

Represents a single node of the Red-Black Tree.

#### Class `RedBlackTree`

Represents the Red-Black Tree and includes methods for manipulating the tree.

Methods inside `RedBlackTree`:

- `pre_order_helper(node)`: Performs pre-order traversal.
- `in_order_helper(node)`: Performs in-order traversal.
- `post_order_helper(node)`: Performs post-order traversal.
- `search_tree_helper(node, key)`: Performs search operation.
- `fix_delete(x)`: Fixes the tree after deletion.
- `rb_transplant(u, v)`: Replaces one subtree as a child of its parent with another subtree.
- `delete_node_helper(node, key)`: Deletes the node with the given key.
- `fix_insert(k)`: Fixes the tree after insertion.
- `insert(key)`: Inserts the key into the tree.
- `get_root()`: Returns the root of the tree.
- `delete_node(data)`: Deletes the node with the given data.
- `print_tree()`: Prints the tree.
- `inorder()`: Performs in-order traversal.
- `postorder()`: Performs post-order traversal.
- `search_tree(k)`: Performs search operation.

## Parameters

- `key`: The value to be stored in a Node.
- `node`: A Node object.
- `data`: The value to be deleted from the tree.
- `x`, `u`, `v`, `k`: These are Node objects used in different methods.

## Return Value

- `get_root()`: Returns the root of the tree.
- `search_tree(k)`: Returns the node with the given key if it exists.

## Usage Examples

```python
rbt = RedBlackTree()
rbt.insert(55)
rbt.insert(40)
rbt.insert(65)
rbt.insert(60)
rbt.insert(75)
rbt.insert(57)
print("In order Traversal: ")
rbt.inorder()
print("Pre order Traversal: ")
rbt.print_tree()
print("Post order Traversal: ")
rbt.postorder()
rbt.delete_node(40)
print("After deleting an element: ")
rbt.inorder()
print("After searching an element: ", rbt.search_tree(55))
```

## Implementation Notes

- The Red-Black Tree implementation uses the color property (represented by an integer) to maintain balance during insertions and deletions.
- Recoloring and rotations are handled appropriately in `fix_insert` and `fix_delete` methods.
- The implementation uses a special TNULL node which is used for initialization of the root node and as the leaves (end) of the tree.