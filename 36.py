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
            self.parent[parent_y] = parent_x
            if parent_y < parent_x or parent_y < self.count[parent_y]:
                self.count[parent_x] += self.count[parent_y]
        
        elif self.rank[parent_x] < self.rank[parent_y]:
            self.parent[parent_x] = parent_y
            if parent_x < parent_y or parent_x < self.count[parent_x]:
                self.count[parent_y] += self.count[parent_x]
        
        else:
            self.parent[parent_y] = parent_x
            self.rank[parent_x] += 1
            if parent_x < parent_y or parent_x < self.count[parent_x]:
                self.count[parent_y] += self.count[parent_x]
    
        return True

    def get_quick(self, x):
        parent_x = self.find(x)

        while True:
            new_x = (parent_x - self.count[parent_x]) % len(self.parent)
            parent_new_x = self.find(new_x)

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
        arr = [(3, 25), (4, 10), (1, 30), (3, 50), (3, 20)] # жадное: 25+20
        self.assertEqual(scheduling(arr), 20)
    
    def test2(self):
        arr = [(1, 10), (2, 20), (3, 30), (4, 40), (4, 50)] # жадное: 40
        self.assertEqual(scheduling(arr), 10)

    def test3(self):
        arr = [(4, 40), (2, 10), (3, 25), (3, 30), (1, 20)] # жадное: 25
        self.assertEqual(scheduling(arr), 10)

if __name__ == "__main__":
    unittest.main()
