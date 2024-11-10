import unittest
import random

class ImplicitTreapNode:
    def __init__(self, val, priority=None):
        self.val = val
        self.priority = priority if priority is not None else random.randint(0, 100)
        self.size = 1
        self.sum = val
        self.left = None
        self.right = None

    def get_size(self, node):
        return node.size if node else 0

    def get_sum(self, node):
        return node.sum if node else 0

    def update(self):
        self.size = 1 + self.get_size(self.left) + self.get_size(self.right)
        self.sum = self.val + self.get_sum(self.left) + self.get_sum(self.right)

class ImplicitTreap:
    def __init__(self):
        self.root = None

    def split_by_size(self, root, k):
        if not root:
            return None, None
        if k <= root.get_size(root.left):
            left, root.left = self.split_by_size(root.left, k)
            root.update()
            return left, root
        else:
            root.right, right = self.split_by_size(root.right, k - root.get_size(root.left) - 1)
            root.update()
            return root, right

    def merge(self, root1, root2):
        if not root1:
            return root2
        if not root2:
            return root1
        if root1.priority < root2.priority:
            root1.right = self.merge(root1.right, root2)
            root1.update()
            return root1
        else:
            root2.left = self.merge(root1, root2.left)
            root2.update()
            return root2

    def insert(self, pos, val):
        new_node = ImplicitTreapNode(val)
        if not self.root:
            self.root = new_node
            return
        root1, root2 = self.split_by_size(self.root, pos)
        self.root = self.merge(self.merge(root1, new_node), root2)

    def erase(self, pos, count=1):
        if not self.root:
            return
        root1, root2 = self.split_by_size(self.root, pos)
        root2, root3 = self.split_by_size(root2, count)
        self.root = self.merge(root1, root3)

    def sum(self, frm, to):
        root1, root2 = self.split_by_size(self.root, frm)
        root2, root3 = self.split_by_size(root2, to - frm + 1)
        res = root2.get_sum(root2)
        self.root = self.merge(self.merge(root1, root2), root3)
        return res


class TestImplicitTreap(unittest.TestCase):
    def setUp(self):
        self.treap = ImplicitTreap()

        self.treap.insert(0, 5)
        self.treap.insert(1, 24)
        self.treap.insert(2, 42)
        self.treap.insert(3, 13)
        self.treap.insert(4, 99)
        self.treap.insert(5, 2)
        self.treap.insert(6, 17)
    
    def test_split_by_size_and_merge(self):
        root1, root2 = self.treap.split_by_size(self.treap.root, 2)
        self.assertEqual(root1.sum, 5 + 24)
        self.assertEqual(root2.sum, 42 + 13 + 99 + 2 + 17)
        
        merged_tree = self.treap.merge(root1, root2)
        self.assertEqual(merged_tree.sum, 5 + 24 + 42 + 13 + 99 + 2 + 17)

    def test_insert_and_erase(self):
        self.treap.insert(4, 30)
        self.assertEqual(self.treap.sum(0, 7), 5 + 24 + 42 + 13 + 30 + 99 + 2 + 17)

        self.treap.erase(4)
        self.assertEqual(self.treap.sum(0, 6), 5 + 24 + 42 + 13 + 99 + 2 + 17)
        self.treap.erase(4, 2)
        self.assertEqual(self.treap.sum(0, 4), 5 + 24 + 42 + 13 + 17)

if __name__ == '__main__':
    unittest.main()