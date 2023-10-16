from colorama import Fore # Color
import json

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

    def removeTail(self):
        if self.tail != None:
            if self.tail.prev != None:
                self.tail = self.tail.prev
                self.tail.next = None
            else:
                self.tail = None
                self.head = None

    def getTailValue(self):
        if self.tail != None:
            return self.tail.val
        return None
    
    def getValAtNode(self, indx):
        if indx > self.count:
            return None
        if self.count/2 < indx:
            d = self.head
            for x in range(indx):
                d = d.next
            return d.val
        else:
            d = self.tail
            for x in range(self.count - 1 - indx):
                d = d.prev
            return d.val

def returnDLLCount(dll):
    t = dll.head
    n = 1
    while t.next != None:
        t = t.next
        n+=1
        
    return n

#Hashmaps are used in form as inbuilt python dictionaries
#The implementation of these hashmaps is used to efficently store subdirectories and files of a certain directory
#Using hashmaps is more efficent than for example a normal list as it allows for more efficent searching/indexing of files and subdirectories

#Trees are used as they make up the whole structure of the file explorer system/class
#Trees are represented in the code as the subdirectories of subdirectories of subdirectories and the files that also pertain to some of those subdirectories
#If you were to visually show all the subdirectories as they are connected in the code, you would see a clear tree/hierarchical structure as the files/directories are connected

#Linked lists are used to record the action history of the user in the file explorer system
#Linked lists are more efficent than an array or an arraylist because the history has to have a dynamic size
#and is more efficent than an arraylist as it dosent have a continous chunk in memory and most operations are much
#more efficent like removing and inserting values and operating on the last values in the list

class File: #File Class
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

class Directory: #Directory Class
    def __init__(self, name, previous):
        self.previous = previous
        self.name = name
        self.subdirectories = {}
        self.files = {}

class FileSystemExplorer: #The Files Explorer Class
    def __init__(self): #initializes by creating a root directory
        self.root = Directory("root", None)
        self.current_directory = self.root

        self.history = DoublyLinkedList()

        self.wait_change_file = None

        self.json_file = "system.json"

    def update_json(self):
        

    def record_history(self, action):
        self.history.append_item(action)

    def create_file(self, name): #Makes a file given the name and content
        if name == "": 
            print("Invalid name")
            return
        file = File(name)
        self.current_directory.files[name] = file
        self.record_history("create:"+name)

    def edit_file(self, name):
        if name == "":
            print("Invalid name")
            return
        if name in self.current_directory.files:
            self.wait_change_file = name
            print(f"Editing file: `{name}`, enter content or submit exit to exit operation")
        else:
            print("File dosent exist")

    def set_edit_changes(self, name, content):
        if content == "exit":
            print("Exiting operation...")
        else:
            self.current_directory.files[name].content = content
            print("Changes created")

    def create_directory(self, name): #Makes a directory given a name
        if name == "":
            print("Invalid name")
            return
        elif name == "/":
            print("Cannot name directory /")
            return
        elif name == "..":
            print("Cannot name directory ..")
            return
        directory = Directory(name, self.current_directory)
        self.current_directory.subdirectories[name] = directory

    def delete_file(self, name):
        if name == "":
            print("Invalid name")
            return
        if self.current_directory.files.get(name) != None:
            self.current_directory.files.pop(name)

    def delete_directory(self, name):
        if name == "":
            print("Invalid name")
            return
        if self.current_directory.subdirectories.get(name) != None:
            self.current_directory.subdirectories.pop(name)

    def cat_file(self, name):
        if name == "":
            print("Invalid name")
            return
        if name in self.current_directory.files:
            if self.current_directory.files[name].content != None:
                print(self.current_directory.files[name].content)

    def change_directory(self, name): #Changes directory 
        if name == "":
            print("Invalid name")
            return
        if name == "/": #return to root
            if self.current_directory != self.root:
                self.current_directory = self.root
        elif name == "..":
            if self.current_directory.previous != None:
                self.current_directory = self.current_directory.previous
        elif name in self.current_directory.subdirectories:
            self.current_directory = self.current_directory.subdirectories[name]
        else:
            print(f"Directory '{name}' not found")

    def list_contents(self):
        for name, directory in self.current_directory.subdirectories.items():
            print(Fore.BLUE + name, end=" ")
        for name, file in self.current_directory.files.items():
            print(Fore.WHITE + name, end=" ")
        print("")

if __name__ == "__main__":
    explorer = FileSystemExplorer()
    
    while True:
        if explorer.wait_change_file != None:
            text = input()
            explorer.set_edit_changes(explorer.wait_change_file, text)
            explorer.wait_change_file = None

        print(Fore.GREEN + f"{explorer.current_directory.name}$", end=" ")
        inpt = input(Fore.WHITE).split()

        try:
            command = inpt[0]
        except IndexError:
            command = ""

        try:
            arg = inpt[1]
        except IndexError:
            arg = ""
        
        if command == "mf":
            explorer.create_file(arg)
        elif command == "edit":
            explorer.edit_file(arg)
        elif command == "mdir":
            explorer.create_directory(arg)
        elif command == "delf":
            explorer.delete_file(arg)
        elif command == "deld":
            explorer.delete_directory(arg)
        elif command == "cat":
            explorer.cat_file(arg)
        elif command == "cd":
            explorer.change_directory(arg)
        elif command == "ls":
            explorer.list_contents()
        elif command == "exit":
            break
        elif command == "help":
            for c, e in [('mf', 'Create a file, takes name argument'), ('edit', 'Edit the contents of a file, takes name argument'), ('mdir', 'Create a dir, takes name argument'), ('delf', 'Delete a file, takes name argument'), ('deld', 'Delete a directory, takes name argument'), ('cat', 'Read contents of a file, takes name argument'), ('cd', 'Change working directory, takes name argument OR / to return to root'), ('ls', 'List file contents'), ('exit', 'Exit the system'), ('help', 'See this page')]:
                print(c + " | " + e)
        else:
            print("Invalid command. Use help for available commands")
