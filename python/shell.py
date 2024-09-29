
import os,re
from termcolor import colored






class CMD():
    
    def __init__(self):
        self.__path: str = os.getcwd()
        self.__cont: bool = True
        
        self.bootloader()
        
        self.main_loop()
        

    def bootloader(self):
        __path = os.getcwd()
        print("Retyk's shell [Version 1.0]\n(c) Herzog Corporation. All rights reserved.")
        print()
    
    
    def digest_input(self,input: str) -> str:
        
        if len(input) == 0:
            return ""
        fields : list[str] = input.split()
        command = fields[0]
        output: str = ""
        # Internal command (hard coded)
        if command == "dir":
            output = self.dir(fields)
        elif command == "exit":
            output = self.exit()
        elif command == "help":
            output = self.help(fields)
        elif command == "cd":
            output = self.cd(fields)
        elif command == "set":
            output = self.set(fields)
        elif command == "cat":
            output = self.cat(fields)
        else:
            output = "unknown command"
        return output
    
    
    def dir(self, fields:list[str]):
        if len(fields) == 1:
            return "\n".join(os.listdir(self.__path))
        fields.remove("dir")
        # Parse variables.
        
        # Field now contains only flag and path (if provided)
        flag, _dir = "",""
        for i in range(len(fields)):
            if "/" in fields[i]:
                # Found flag.
                flag = fields[i]
                fields.remove(flag)
                break
            
        # At this point only the directory value is in the list. 
        if len(fields) == 0: # No dir given
            _dir = '.'
        else:
            _dir = fields[0]
        
        if not os.path.isdir(_dir):
            return ErrorMessage("dir", 1, _dir).get_msg()
        
        if flag == "": # No flags:
            return "\n".join(os.listdir(_dir))
        if flag == "/s": # Recursive
            return_msg = f"{_dir}:"
            listdir = os.listdir(_dir)
            for file in listdir:
                return_msg += '\n'
                if os.path.isdir(file):
                    return_msg += '\n'
                    return_msg += self.dir(["dir", file, "/s"])
                else:
                    return_msg += file
                
            return return_msg
        else:
            return ErrorMessage("dir",0).get_msg()
        
    def exit(self):
        self.__cont = False
        return "Bye Bye Bye"
    
    def cd(self,args: list[str]) -> str:
        
        if len(args) == 1:
            return ""
        if len(args) == 2:
            path = args[1]
        else:
            return ErrorMessage("cd", 0).get_msg()
        
        if os.path.isabs(path): # Absolute path was given
            self.__path = path
            return ""
        # Relative path
        
        init_path = self.__path # Backup path incase one of the directories doesn't exist
        
        for directory in path.split("/"):
            
            if directory == '.':
                pass # Path is the same
            elif directory == "..": # Backtrack one directory
                if re.search("/.*/",self.__path): 
                    self.__path = "/".join(self.__path.split("/")[:-1])
                else:
                    pass
            else:
                if os.path.isdir(self.__path + "/" + directory):
                    self.__path += '/'
                    self.__path += directory
                else:
                    self.__path = init_path
                    return ErrorMessage("cd",1,directory).get_msg()

        return ""
    
    def set(self, args) -> str:
        return ""
    
    def help(self, args: list[str]) -> str:
        if len(args) == 1:
            return "These shell commands are defined internally.\nFor additional info about each command type help <command>\nset,cd,dir,exit"
        elif len(args) == 2:
            return man(args[1])
        else:
            return ErrorMessage("help",0).get_msg()
    
    def cat(self,args:list[str]) -> str:
        if len(args) == 1 or len(args) > 3:
            return ErrorMessage("cat",0).get_msg()
        if len(args) == 2:
            fpath = args[1]
        args.remove("cat")
        # Parse variables.
        # Field now contains only flag and path (if provided)
        flag, fpath = "",""
        for i in range(len(args)):
            if "/" in args[i]:
                # Found flag.
                flag = args[i]
                args.remove(flag)
                break
        fpath = self.__path + "/" + args[0]
        
        if (not os.path.isfile(fpath)):
            return ErrorMessage("cat",1 ,fpath).get_msg()
        
        try:
            if not flag: # No flags provided
                with open(fpath,'r') as file:
                    return file.read()
            elif flag == "/n": # n flag - numbers the lines.
                with open(fpath,'r') as file:
                    lines = file.read().splitlines()
                    numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
                    return "\n".join(numbered_lines)
            else: 
                return ErrorMessage("cat",0).get_msg()
        except UnicodeDecodeError as err:
            return "format not supported"
    def main_loop(self):
        while self.__cont:
            user_input = input(f"{self.get_path_str()}>>>")
            print(self.digest_input(user_input))
    
    
    def get_path_str(self):
        return colored("Retyk@","green") + colored(str(self.__path),"red")


def man(name):
        if name == "dir":
            return "Display content of directory\nUsage - dir <flag> <path> \nDefault Values:\npath = current path \n\nflag explanation --\n/s - recursive"
        if name == "cd":
            return "Change current directory\nUsage - cd <path>\n\nNo flags supported"
        if name == "help":
            return "Get help\nUsage - help <command>\nDefault Values:\ncommand = help\n\nNo flags supported"
        if name == "cat":
            return "Display content of file\nUsage - cat <flag> <path> \n\nflag explanation --\n/n - number output lines"
        return ""

class ErrorMessage():
    __msg: str = ""
    def __init__(self, name :str, code: int, *args) -> None:
        if name == "dir":
            if code == 0:
                self.__msg = "Syntax Error \n" + man("dir")
            elif code == 1:
                self.__msg = f"Directory of {args[0]}\n File  Not Found"
        
        elif name == "cd":
            if code == 0:
                self.__msg = "Syntax Error \n" + man("cd")
            if code == 1:
                self.__msg = f"cd: File or Directory not found: " + args[0]
        
        elif name == "help":
            if code == 0:
                self.__msg = "Syntax Error \n" + man("help")
        
        elif name == "cat":
            if code == 0:
                self.__msg = "Syntax Error \n" + man(name)
            elif code == 1:
                self.__msg = f"File {args[0]} Not Found"

    
    def get_msg(self) -> str:
        return self.__msg
    
    



def main():
    cmd = CMD()



if __name__ == "__main__":
    main()

