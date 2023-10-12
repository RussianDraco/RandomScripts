"""
X 8. Write a Python program to create a doubly linked list, append some items and iterate through the list (print forward).
X 9. Write a Python program to create a doubly linked list and print nodes from current position to first node.
X 10. Write a Python program to count the number of items of a given doubly linked list.
X 11. Write a Python program to print a given doubly linked list in reverse order.
X 12. Write a Python program to insert an item in front of a given doubly linked list.
X 13. Write a Python program to search a specific item in a given doubly linked list and return true if the item is found otherwise return false.
X 14. Write a Python program to delete a specific item from a given doubly linked list.
"""
class dNode:
    def __init__(self, v, p = None, n = None):
        self.val = v
        self.prev = p
        self.next = n

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def append_item(self, data):
        new = dNode(data)
        if self.head == None:
            self.head = new
            self.tail = new
        else:
            new.prev = self.tail
            self.tail.next = new
            self.tail = new

        self.count += 1

    def printForward(self):
        t = self.head
        for x in range(self.count):
            print(t.val)
            t = t.next

    def printBackward(self):
        t = self.tail
        for x in range(self.count):
            print(t.val)
            t = t.prev

    def appendAtFront(self, data):
        new = dNode(data)
        if self.head == None:
            self.head = new
            self.tail = new
        else:
            new.next = self.head
            self.head.prev = new
            self.head = new

        self.count += 1

    def valueInList(self, val):
        t = self.head
        for x in range(self.count):
            if t.val == val:
                return True
            t = t.next
        return False
    
    def removeValue(self, val):
        t = self.head
        for x in range(self.count):
            if t.val == val:
                if t == self.head: #trying to remove head
                    if self.head.next == None: #theres only one value
                        self.head = None
                    else: #theres more than one
                        self.head = self.head.next
                        self.head.prev = None
                else: #not trying to remove head
                    before_t = t.prev
                    after_t = t.next

                    if before_t != None:
                        before_t.next = after_t
                    if after_t != None:
                        after_t.prev = before_t
                self.count -= 1
                return
            t = t.next

def returnDLLCount(dll):
    t = dll.head
    n = 1
    while t.next != None:
        t = t.next
        n+=1
        
    return n

dll = DoublyLinkedList()

dll.append_item("a")
dll.append_item("b")
dll.append_item("c")

dll.printForward()
dll.printBackward()

dll.removeValue("a")

dll.printForward()

dll.removeValue("b")

dll.printForward()

dll.removeValue("c")

dll.printForward()