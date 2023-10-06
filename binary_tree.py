import random

class Node:
    def __init__(self, data, left = None, right = None, depth = 0):
        self.left = left
        self.right = right
        self.data = data
        self.depth = depth

    def insert(self, data):
        if self.data == None:
            self.data = data
        else:
            if data < self.data:
                if self.left == None:
                    self.left = Node(data, depth = self.depth + 1)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right == None:
                    self.right = Node(data, depth = self.depth + 1)
                else:
                    self.right.insert(data)

    def getChildren(self):
        return ((self.left if self.left != None else None), (self.right if self.right != None else None))

    def printMyNodes(self):
        print_array = [self]
        for x in range(self.findTreeHeight()):
            for y in print_array[x]:
                childs = y.getChildren()
                if childs[0] != None:
                    print_array[x + 1].append(childs[0])
                if childs[1] != None:
                    print_array[x + 1].append(childs[1])

    def findTreeHeight(self):
        if self.left == None:
            l = self.depth
        else:
            l = self.left.findTreeHeight()
        if self.right == None:
            r = self.depth
        else:
            r = self.right.findTreeHeight()

        return max(l, r)

tree = Node(1000)

for x in range(0, 50):
    tree.insert(random.randint(0, 1000))

tree.printMyNodes()

print("Total height: " + str(tree.findTreeHeight()))