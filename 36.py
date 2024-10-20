import unittest

class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n + 1)]
        self.rank = [0] * (n + 1)
        self.count = [0] * (n + 1)

    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        parent_x = self.find(x)
        parent_y = self.find(y)

        if parent_x == parent_y:
            return False

        if self.rank[parent_x] > self.rank[parent_y]:
            self.update_p_c(parent_y, parent_x)
        elif self.rank[parent_x] < self.rank[parent_y]:
            self.update_p_c(parent_x, parent_y)
        else:
            self.rank[parent_x] += 1
            self.update_p_c(parent_y, parent_x)

        return True

    def update_p_c(self, child, parent):
        self.parent[child] = parent
        if child < parent or parent < self.count[parent]:
            self.count[parent] += self.count[child]

    def get_quick(self, x):
        parent_x = self.find(x)

        new_x = (parent_x - self.count[parent_x]) % len(self.parent)
        parent_new_x = self.find(new_x)

        if parent_new_x == 0:
            return 0

        if self.count[parent_new_x] == 0:
            self.count[parent_new_x] += 1
            return parent_new_x

        self.union(parent_x, parent_new_x)
        return self.get_quick(self.find(parent_new_x))

def scheduling(tasks):
    tasks.sort(key=lambda t: (-t[1], t[0]))
    max_deadline = max(t[0] for t in tasks)
    uf = UnionFind(max_deadline)
    schedule = [None] * max_deadline
    total_fine = 0

    for deadline, fine in tasks:
        parent = uf.find(deadline)
        free_day = uf.get_quick(parent)

        if free_day == 0 or free_day > deadline:
            total_fine += fine
        else:
            schedule[free_day - 1] = deadline, fine
            uf.union(free_day, parent)

    return total_fine


class TestScheduling(unittest.TestCase):

    def test1(self):
        arr = [(3, 25), (4, 10), (1, 30), (3, 50), (3, 20)] # жадное: 30
        self.assertEqual(scheduling(arr), 20)

    def test2(self):
        arr = [(1, 10), (2, 20), (3, 30), (4, 40), (4, 50)] # жадное: 30
        self.assertEqual(scheduling(arr), 10)

    def test3(self):
        arr = [(4, 40), (2, 10), (3, 25), (3, 30), (1, 20)] # жадное: 30
        self.assertEqual(scheduling(arr), 10)

    def test4(self):
        arr = [(1, 10), (2, 10), (3, 10), (4,10), (5,10), (6,10), (9, 10), (9, 15), (9, 15), (9, 15), (10, 5), (10, 10)] # жадное: 30
        self.assertEqual(scheduling(arr), 15)

if __name__ == "__main__":
    unittest.main()

