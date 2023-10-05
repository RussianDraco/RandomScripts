class Node:
    def __init__(self, v, n):
        self.val = v
        self.next = n
c = Node("C", None)
b = Node("B", c)
a = Node("A", b)

def printAll(startNode):
    t = startNode
    while t:
        print(t.val)
        t = t.next
def addTailVal(startNode, data):
    l = startNode
    while l.next:
        l = l.next
    n = Node(data, None)
    l.next = n
    return startNode
def addHeadVal(startNode, data):
    n = Node(data, startNode)
    return n
def changeAtIndex(startNode, index, newData):
    t = startNode
    for x in range(index):
        t = t.next
    t.val = newData
    return startNode
def removeAtIndex(startNode, index):
    ta = None
    tb = startNode
    for x in range(index):
        ta = tb
        tb = ta.next
    ta.next = tb.next
    return startNode
def insertAtIndex(startNode, index, data):
    ta = None
    tb = startNode
    for x in range(index):
        ta = tb
        tb = ta.next
    t = Node(data, tb)
    ta.next = t
    return startNode
def linkSize(startNode):
    l = startNode
    n = 0
    while l.next:
        l = l.next
        n+=1
    return n + 1
print(linkSize(Node("A", None)))