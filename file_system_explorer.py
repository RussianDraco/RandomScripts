from colorama import Fore # Color
import json
import os

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
    
    def getValueBeforeTail(self):
        if self.tail != None:
            if self.tail.prev != None:
                return self.tail.prev.val
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

    #gives copy of this file with contents
    def copy(self):
        return File(self.name, self.content)

class Directory: #Directory Class
    def __init__(self, name, previous):
        self.previous = previous
        self.name = name
        self.subdirectories = {}
        self.files = {}

    #a function to get info for the formation of the json file, returns a dict of its subdirs get_dir_dict and its files
    #runs recursively when subdirs are present
    def get_dir_dict(self): 
        out = {}
        for name, directory in self.subdirectories.items():
            out["/" + name] = directory.get_dir_dict()

        for name, file in self.files.items():
            out[name] = file.content

        return out
    
    #provide an identical copy of the directory with identical contents, used for copy/pasting so that pointers dont point back to original
    def copy(self, copyPrev):
        copyDir = Directory(self.name, copyPrev)
        if len(self.subdirectories) > 0:
            for dname, subdir in self.subdirectories.items():
                c = subdir.copy(copyDir)
                copyDir.subdirectories[dname] = c
        if len(self.files) > 0
            for fname, file in self.files.items():
                c = file.copy()
                copyDir.files[fname] = c
        return copyDir

class FileSystemExplorer: #the file system explorer
    def __init__(self): #initializes file system by creating a root directory
        self.root = Directory("root", None)
        self.current_directory = self.root

        self.history = DoublyLinkedList() #a series of hashmaps that contain all information about the files/directories, used for undo function

        self.wait_change_file = None #variable used for editing files

        self.json_file = "system.json" #file containing the files/directories to hold info in storage between runs of this script

        self.path_string = "/root" #starting path

        self.copied_file = None #used to store copied files/dirs

    def update_json(self, returnDict = False): #function to update system.json with files/dirs after every command
        data = {"/root":self.root.get_dir_dict()}

        with open(self.json_file, 'w') as jf:
            json.dump(data, jf)
        jf.close()

    #converts a dictionary into directories with subdirectories and files with content, used for loading json file info into system explorer
    def json_dir_conv(self, dirName, dirDict, prevDir):
        thisDir = Directory(dirName, prevDir)

        out = {}
        for key, value in dirDict.items():
            if "/" in key:
                thisDir.subdirectories[key.replace("/", "")] = self.json_dir_conv(key.replace("/", ""), value, thisDir)
            else:
                thisDir.files[key] = File(key, value)

        return thisDir

    def load_system_dict(self, pathString, dict): #function to load a dictionary into the file system, usually used for loading in history snapshots(undo command)
        for key, value in dict.items():
            new_root = self.json_dir_conv(key, value, None)

        self.path_string = pathString
        self.root = new_root

        if pathString == "/root":
            self.current_directory = self.root
        else:
            currentDir = self.root
            for d in pathString.replace("/root", "")[1:].split("/"):
                currentDir = currentDir.subdirectories[d]

            self.current_directory = currentDir

    def load_json(self): #complete function to load system.json into file explorer
        with open(self.json_file, 'r') as jf:
            data = json.load(jf)
        jf.close()

        for key, value in data.items():
            new_root = self.json_dir_conv(key, value, None)

        self.path_string = "/root"
        self.root = new_root
        self.current_directory = self.root

    #function to save a snapshot of the current file explorer into the history linked list
    #snap is used when sometimes the history snapshot was already calculated elsewhere in code and provided to this function to avoid redundant recalculations
    def snapshot_history(self, snap = None):
        if snap != None:
            self.history.append_item(snap)
            return
        self.history.append_item((self.path_string, {"/root":self.root.get_dir_dict()}))

    def create_file(self, name): #creates a file in the current working directory with a name and empty content
        if name == "": 
            print("Invalid name")
            return
        elif '/' in name:
            print("Cannot include / in file name")
            return
        elif self.current_directory.subdirectories.get(name) != None:
            print("Directory with same name already exists")
            return
        file = File(name)
        self.current_directory.files[name] = file

    def copy_file(self, name): #function to copy a file or directory, sets the copied_file field to that file/dir
        if (f := self.current_directory.subdirectories.get(name)) != None:
            self.copied_file = f
        elif (f := self.current_directory.files.get(name)) != None:
            self.copied_file = f
        else:
            print("File or directory with such name dosent exist")

    def paste_file(self): #pastes the copied_file field into the current working directory
        if self.copied_file != None:
            if self.copied_file.name in self.current_directory.subdirectories or self.copied_file.name in self.current_directory.files:
                print("File or directory with such name already exists in this directory")
                return

            copied_is_dir = False
            try:
                temp = self.copied_file.files
                copied_is_dir = True
            except AttributeError:
                pass
            
            if copied_is_dir:
                self.current_directory.subdirectories[self.copied_file.name] = self.copied_file.copy(self.current_directory)
            else:
                self.current_directory.files[self.copied_file.name] = self.copied_file

        else:
            print("No file or directory has been copied")

    def move_file(self, arg): #moves a file/dir from the current working directory to the defined path, i.e. file named A in /root folder moved to /root/cool/A
        moving_objName = arg.split('/')[-1]
        moving_obj = None
        file_is_dir = False

        if (f := self.current_directory.subdirectories.get(moving_objName)) != None:
            moving_obj = f
            file_is_dir = True
        elif (f := self.current_directory.files.get(moving_objName)) != None:
            moving_obj = f
        else:
            print(f"File or directory with name {moving_objName} dosent exist in current working directory")
            return

        end_path = arg.replace("/" + moving_objName, "")
        end_dir = None

        if end_path == "/root":
            end_dir = self.root
        else:
            end_dir = self.root
            print(end_path)
            for d in end_path.replace("/root", "")[1:].split("/"):
                print(str(end_path.replace("/root", "")[1:].split("/")))
                end_dir = end_dir.subdirectories[d]

        if moving_objName in end_dir.subdirectories or moving_objName in end_dir.files:
            print("Object with such name already exists in destination directory")
            return

        if file_is_dir:
            end_dir.subdirectories[moving_objName] = moving_obj
            self.current_directory.subdirectories.pop(moving_objName)
        else:
            end_dir.files[moving_objName] = moving_obj
            self.current_directory.files.pop(moving_objName)

    def edit_file(self, name): #function to edit the contents of a file, asks for a prompt and then creates changes with set_edit_changes
        if name == "":
            print("Invalid name")
            return
        if name in self.current_directory.files:
            self.wait_change_file = name
            print(f"Editing file: `{name}`, enter content or submit exit to exit operation")
        else:
            print("File dosent exist")

    def set_edit_changes(self, name, content): #system function that applies the edit input into the file
        if content == "exit":
            print("Exiting operation...")
        else:
            self.current_directory.files[name].content = content
            print("Changes created")

    def create_directory(self, name): #makes a directory given a name
        if name == "":
            print("Invalid name")
            return
        elif '/' in name:
            print("Cannot include / in directory name")
            return
        elif name == "..":
            print("Cannot name directory ..")
            return
        elif self.current_directory.files.get(name) != None:
            print("File with same name already exists")
            return
        directory = Directory(name, self.current_directory)
        self.current_directory.subdirectories[name] = directory

    def delete_file(self, name): #deletes a file from cwd
        if name == "":
            print("Invalid name")
            return
        if self.current_directory.files.get(name) != None:
            self.current_directory.files.pop(name)

    def delete_directory(self, name): #delete a dir from cwd
        if name == "":
            print("Invalid name")
            return
        if self.current_directory.subdirectories.get(name) != None:
            self.current_directory.subdirectories.pop(name)

    def cat_file(self, name): #read the contents of a file
        if name == "":
            print("Invalid name")
            return
        if name in self.current_directory.files:
            if self.current_directory.files[name].content != None:
                print(self.current_directory.files[name].content)

    def change_directory(self, name): #changes cwd
        if name == "":
            print("Invalid name")
            return
        if name == "/": #return to root
            if self.current_directory != self.root:
                self.current_directory = self.root
            self.path_string = "/root"
        elif name == "..":
            if self.current_directory.previous != None:
                self.path_string = self.path_string.replace("/" + self.current_directory.name, "")
                self.current_directory = self.current_directory.previous
        elif name in self.current_directory.subdirectories:
            self.current_directory = self.current_directory.subdirectories[name]
            self.path_string += "/" + self.current_directory.name
        else:
            print(f"Directory '{name}' not found")

    def list_contents(self): #lists the contents of a file, all subdirs and files
        for name, directory in self.current_directory.subdirectories.items():
            print(Fore.BLUE + name, end=" ")
        for name, file in self.current_directory.files.items():
            print(Fore.WHITE + name, end=" ")
        print("")

if __name__ == "__main__": #main run function
    explorer = FileSystemExplorer() #inits the file system explorer class

    explorer.snapshot_history() #creates an init history snapshot

    while True: #main running loop
        if explorer.wait_change_file != None: #if the system is waiting for the contents of a file to be inputted, handle that
            text = input()
            explorer.set_edit_changes(explorer.wait_change_file, text)
            explorer.wait_change_file = None

        print(Fore.GREEN + f"{explorer.path_string}$", end=" ") #prints the cwd path
        inpt = input(Fore.WHITE).split() #gets input from the user

        #gets the command part of the input, if there is an exception(there is no command), set it to an empty str
        try:
            command = inpt[0]
        except IndexError:
            command = ""

        #gathers any argument that was also given with a command, usually a name argument
        try:
            arg = inpt[1]
        except IndexError:
            arg = ""
        
        #checks through all possible commands that is inputted or otherwise reply that its not a real command and advise to use help command
        if command == "mf":
            explorer.create_file(arg)
        elif command == "edit":
            explorer.edit_file(arg)
        elif command == "copy":
            explorer.copy_file(arg)
        elif command == "paste":
            explorer.paste_file()
        elif command == "mv":
            explorer.move_file(arg)
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
        elif command == "load":
            explorer.load_json()
        elif command == "undo":
            lastHistorySnap = explorer.history.getValueBeforeTail()
            if lastHistorySnap != None:
                lastPathStr, lastSysDict = lastHistorySnap
                explorer.load_system_dict(lastPathStr, lastSysDict)
                explorer.history.removeTail()
            else:
                print("No history before this")
        elif command == "exit":
            break
        elif command == "help":
            for c, e in [('mf', 'Create a file, takes name argument'), ('copy', 'Copy a file or directory, takes name argument'), ('paste', 'Paste the last copied file or directory into current working directory'), ('mv', 'Move a file or directory, takes a location/name argument of file in new location'), ('edit', 'Edit the contents of a file, takes name argument'), ('mdir', 'Create a dir, takes name argument'), ('delf', 'Delete a file, takes name argument'), ('deld', 'Delete a directory, takes name argument'), ('cat', 'Read contents of a file, takes name argument'), ('cd', 'Change working directory, takes name argument OR / to return to root'), ('ls', 'List file contents'), ('load', 'Load the file system from the last saved snapshot'), ('undo', 'Undo your last action'), ('exit', 'Exit the system'), ('help', 'See this page')]:
                print(c + " | " + e)
        else:
            print("Invalid command. Use help for available commands")

        #update the system.json file and update the history linked list if something changed
        explorer.update_json()
        if (snap := (explorer.path_string, {"/root":explorer.root.get_dir_dict()})) != explorer.history.getTailValue():
            explorer.snapshot_history(snap)
