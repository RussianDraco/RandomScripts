from colorama import Fore # Color

#Hashmaps are used in form as inbuilt python dictionaries
#The implementation of these hashmaps is used to efficently store subdirectories and files of a certain directory
#Using hashmaps is more efficent than for example a normal list as it allows for more efficent searching/indexing of files and subdirectories

#Trees are used as they make up the whole structure of the file explorer system/class
#Trees are represented in the code as the subdirectories of subdirectories of subdirectories and the files that also pertain to some of those subdirectories
#If you were to visually show all the subdirectories as they are connected in the code, you would see a clear tree/hierarchical structure as the files/directories are connected

class File: #File Class
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

class Directory: #Directory Class
    def __init__(self, name):
        self.name = name
        self.subdirectories = {}
        self.files = {}

class FileSystemExplorer: #The Files Explorer Class
    def __init__(self): #initializes by creating a root directory
        self.root = Directory("root")
        self.current_directory = self.root

    def create_file(self, name, content=""): #Makes a file given the name and content
        file = File(name, content)
        self.current_directory.files[name] = file

    def create_directory(self, name): #Makes a directory given a name
        directory = Directory(name)
        self.current_directory.subdirectories[name] = directory

    def delete_file(self, name):
        if self.current_directory.files.get(name) != None:
            self.current_directory.files.pop(name)

    def delete_directory(self, name):
        if self.current_directory.subdirectories.get(name) != None:
            self.current_directory.subdirectories.pop(name)

    def change_directory(self, name): #Changes directory 
        if name == "..": #move up one level
            if self.current_directory != self.root:
                self.current_directory = self.root
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
        print(Fore.GREEN + f"{explorer.current_directory.name}$", end=" ")
        command = input(Fore.WHITE).split()
        
        if command[0] == "mf":
            explorer.create_file(command[1])
        elif command[0] == "mdir":
            explorer.create_directory(command[1])
        elif command[0] == "delf":
            explorer.delete_file(command[1])
        elif command[0] == "deld":
            explorer.delete_directory(command[1])
        elif command[0] == "cd":
            explorer.change_directory(command[1])
        elif command[0] == "ls":
            explorer.list_contents()
        elif command[0] == "exit":
            break
        elif command[0] == "help":
            for c, e in [('mf', 'Create a file, takes name argument'), ('mdir', 'Create a dir, takes name argument'), ('delf', 'Delete a file, takes name argument'), ('deld', 'Delete a directory, takes name argument'), ('cd', 'Change working directory, takes name argument OR .. for step up'), ('ls', 'List file contents'), ('exit', 'Exit the system'), ('help', 'See this page')]:
                print(c + " | " + e)
        else:
            print("Invalid command. Use help for available commands")
