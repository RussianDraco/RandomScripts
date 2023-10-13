from colorama import Fore

class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

class Directory:
    def __init__(self, name):
        self.name = name
        self.subdirectories = {}
        self.files = {}

class FileSystemExplorer:
    def __init__(self):
        self.root = Directory("root")
        self.current_directory = self.root

    def create_file(self, name, content=""):
        file = File(name, content)
        self.current_directory.files[name] = file

    def create_directory(self, name):
        directory = Directory(name)
        self.current_directory.subdirectories[name] = directory

    def change_directory(self, name):
        if name == "..":
            # Move up one level
            if self.current_directory != self.root:
                self.current_directory = self.root
        elif name in self.current_directory.subdirectories:
            self.current_directory = self.current_directory.subdirectories[name]
        else:
            print(f"Directory '{name}' not found.")

    def list_contents(self):
        #print("Contents of", self.current_directory.name)
        for name, directory in self.current_directory.subdirectories.items():
            print(Fore.BLUE + name, end=" ")
        for name, file in self.current_directory.files.items():
            print(Fore.RED + name, end=" ")
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
        elif command[0] == "cd":
            explorer.change_directory(command[1])
        elif command[0] == "ls":
            explorer.list_contents()
        elif command[0] == "exit":
            break
        elif command[0] == "help":
            for x in [('mf', 'Create a file, takes name argument'), ('mdir', 'Create a dir, takes name argument'), ('cd', 'Change working directory, takes name argument OR .. for step up'), ('ls', 'List file contents'), ('exit', 'Exit the system'), ('help', 'See this page')]:
                c, e = x
                print(c + " | " + e)
        else:
            print("Invalid command. Use help for available commands")
