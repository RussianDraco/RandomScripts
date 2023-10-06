import random

class Node:
    def __init__(self, data, left = None, right = None):
        self.left = left
        self.right = right
        self.data = data

    def insert(self, data):
        if self.data == None:
            self.data = data
        else:
            if data < self.data:
                if self.left == None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right == None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)

    def printMyNodes(self):
        print(self.data)
        if self.left:
            self.left.printMyNodes()
        if self.right:
            self.right.printMyNodes()

tree = Node(1000)

for x in range(0, 50):
    tree.insert(random.randint(0, 1000))

tree.printMyNodes()