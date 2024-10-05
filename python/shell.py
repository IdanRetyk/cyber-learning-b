import os,re,subprocess,random
from termcolor import colored


class CMD():
    # Singleton
    def __init__(self):
        self.__outpath: str = ""
        self.__inpath: str = ""
        self.__input : str = ""
        self.__output: str = ""
        self.__path: str = os.getcwd().replace('\\','/') # Any os will use forward slash (windows supports )
        self.__cont: bool = True
        self.__my_path: str = os.environ["PATH"] + "/Users/Idan/cyber-learning-b/python;/Users/Idan/downloads;"
        
        self.interals: list[str] = ["dir","exit","help","cd","set","cat","md","rm"]
        
        
        self.bootloader()
        
        self.main_loop()
        

    def bootloader(self):
        print("Retyk's shell [Version 1.0]\n(c) Herzog Corporation. All rights reserved.")
        print()
    
    
    def digest_input(self,input: str) -> str:
        
        if len(input) == 0:
            return ""
        outpath,inpath = "",""
        if '|' in input:
            first,second = input.split('| ')
            self.handle_pipe(first,second)
            return ""
        if '>' in input:
            input,outpath = input.split('> ')
        if '<' in input:
            input,inpath = input.split('< ')
        if '<' in outpath:
            outpath,inpath = outpath.split('< ')

        fields : list[str] = input.split()
        command = fields[0]
        output: str = ""
        # Internal command (hard coded)
        if command in self.interals:
            output = eval(f'self.{command}(fields)') 
        else:
            # External command
            self.__inpath,self.__outpath = inpath,outpath
            output = self.run_external(fields)
            if output:
                return output
            else:
                return ""
        
        if outpath: # if output is redirected
            with open(self.__path + '/' + outpath,'w') as file:
                file.write(output)
            return ""
        else:
            return output
    
    def handle_pipe(self,first :str,second: str):
        if first.split()[0] in self.interals: # If first command is internal simply call digest input twice.
            file_name = str(random.randint(1000,9999)) + 'txt'
            while os.path.isfile(self.__path + '/' + file_name):
                file_name = str(random.randint(1000,9999)) + '.txt'
            self.digest_input(f"{first} > {file_name}")
            to_return =  self.digest_input(f"{second} < {file_name}")
            os.remove(self.__path + '/' + file_name)
            return to_return
        
        if second.split()[0] in self.interals: # If second command is internal, perform the first command without any output, and than the second one as usual
                                                #as none of the internal commands support input redirect.
            self.digest_input(f"{first}")
            return self.digest_input(f"{second}")
        
        # If both are external.
        
        # open p1
        found_file: bool = False
        for path in (self.__my_path.split(";") + [self.__path]):
            cmd_input = first.split()
            command_name = cmd_input[0]
            if os.path.isfile(path + '/' + command_name) and not found_file:
                found_file = True
                if ".py" in command_name: 
                    p1: subprocess.Popen[str] = subprocess.Popen(["python"] + cmd_input,cwd=path,text=True,stdin=None,stdout=subprocess.PIPE) 
                elif ".exe" in command_name:
                    p1 = subprocess.Popen(cmd_input,cwd=path,text=True,stdin=None,stdout=subprocess.PIPE) 
                else:
                    print("Unkown command")
        # open p2
        found_file: bool = False
        for path in (self.__my_path.split(";") + [self.__path]):
            command_name = second.split()[0]
            if os.path.isfile(path + '/' + command_name) and not found_file:
                found_file = True
                if ".py" in command_name: 
                    p2 = subprocess.Popen("python " + second,cwd=path,text=True,stdin=p1.stdout)  # type: ignore
                elif ".exe" in command_name:
                    p2 = subprocess.Popen(second,cwd=path,text=True,stdin=p1.stdout) # type: ignore
                else:
                    print("Unkown command")
        
        p1.stdout.close() # type:ignore
        print("Before communicate")
        try:
            outs, errs = p2.communicate() # type:ignore
            print("After Communicate")
            if outs:
                print(outs)

        except subprocess.TimeoutExpired:
            p2.kill() # type:ignore
            outs, errs = p2.communicate() # type:ignore
        
        
    
    def dir(self, fields:list[str]) -> str:
        if len(fields) == 1: # User typed ""dir""
            return "\n".join(os.listdir(self.__path))
        fields.remove("dir")
        # Parse variables.
        
        if len(fields) > 4:
            return ErrorMessage("dir",0).get_msg()
        
        
        
        # Field now contains only flag and path (if provided)
        flag, _dir,file_type = "","",""
        for i in range(len(fields)):
            if "-" in fields[i] and not '/' in fields[i]:
                # Found flag.
                flag = fields[i]
            
            if re.match(r"\*\.",fields[i]):
                file_type = "." + fields[i].split('.')[-1]
        
        if flag:
            fields.remove(flag)
        if file_type:
            fields.remove(f"*{file_type}")
        # At this point only the directory value is in the list. 
        if len(fields) == 0: # No dir given
            _dir = self.__path
        else:
            _dir = fields[0]
            if not os.path.isdir(_dir):
                return ErrorMessage("dir", 1, _dir).get_msg()
        
        if flag == "": # No flags:
            return "\n".join([i for i in os.listdir(_dir) if file_type in i])
        if flag == "-s": # Recursive
            return_msg = f"{_dir.split('/')[-1]}:"
            listdir = os.listdir(_dir)
            for file in listdir:
                
                if os.path.isdir(_dir + '/' + file):
                    return_msg += '\n'
                    return_msg += self.dir(["dir", _dir + '/' + file, "-s",f"*{file_type}"])
                    return_msg += '\n'
                else:
                    if file_type in file:
                        return_msg += '\n'
                        return_msg += file
                
            return return_msg
        else:
            return ErrorMessage("dir",0).get_msg()
        
    def exit(self, fields: list[str]):
        self.__cont = False
        return "Bye Bye Bye"
    
    def cd(self, args: list[str]) -> str:
        
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
            
            if directory == '.': # Path is the same
                print(self.__path) 
            elif directory == "..": # Backtrack one directory
                if re.search("/.*/",self.__path): # If there is only one directory left, don't backtrack.
                    self.__path = "/".join(self.__path.split("/")[:-1])
            else:
                if os.path.isdir(self.__path + "/" + directory):
                    self.__path += '/'
                    self.__path += directory
                else:
                    self.__path = init_path
                    return ErrorMessage("cd",1,directory).get_msg()

        return ""
    
    def set(self, args: list[str]) -> str:
        if len(args) == 1:
            return "\n".join(f"{k} = {v}" for k,v in os.environ.items())
        
        env_var = args[2].split('=')
        var_name = env_var[0]
        
        if len(env_var) == 1:
            try:
                content = os.environ[var_name]
                
                for key in os.environ:
                    if key.lower() == var_name.lower():
                        var_name = key
                        break
                
                return f"{var_name} = {content}"
            except KeyError:
                return ErrorMessage("set",1,var_name).get_msg()
        
        else:
            env_var_val = "=".join(env_var[1:])
            if env_var_val == "":
                try:
                    del os.environ[var_name]
                except KeyError:
                    pass
                else:
                    os.environ[var_name] = env_var_val
        
        return ""
    
    def help(self, args: list[str]) -> str:
        if len(args) == 1:
            return "These shell commands are defined internally.\nFor additional info about each command type help <command>\nset,cd,dir,exit,rm,cat,md"
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
            if "-" in args[i]:
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
            elif flag == "-n": # n flag - numbers the lines.
                with open(fpath,'r') as file:
                    lines = file.read().splitlines()
                    numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
                    return "\n".join(numbered_lines)
            else: 
                return ErrorMessage("cat",0).get_msg()
        except UnicodeDecodeError as err:
            return "format not supported"
        except FileNotFoundError:
            return ErrorMessage("cat",1,fpath).get_msg()
    
    def md(self,args: list[str]) -> str:
        if len (args) == 1 or len(args) > 3:
            return ErrorMessage("md",0).get_msg()
        if len (args) == 2: # Only name was given
            if not '/' in args[1]:
                flag,name = "",args[1]
            else:
                return "Syntax Error"
        else: # Name and flag
            if '-' in args[1]:
                flag,name = args[1],args[2]
            elif '-' in args[2]:
                flag,name = args[2], args[1]
            else:
                return "Syntax Error"

        if flag == "":
            os.makedirs(self.__path +'/' + name)
            return ""
        elif flag == "-c":
            os.makedirs(self.__path +'/' + name)
            self.cd(["cd",name])
            return ""
        else:
            return ErrorMessage("md",0).get_msg()
    
    def rm(self,args: list[str]) -> str:
        if len (args) == 1 or len(args) > 2:
            return ErrorMessage("rm",0).get_msg()
        else:
            name = args[1]
            if os.path.isdir(self.__path + '/' + name):
                os.removedirs(self.__path + '/' + name)
                return f"deleted directory {name} "
            else:
                return ErrorMessage("rm",1,name).get_msg()
            
    def run_external(self,cmd_input: list[str]) -> str:
        if len(cmd_input) == 0:
            return ErrorMessage("external",0).get_msg()
        
        if self.__outpath:
            fout = open(self.__path + '/' + self.__outpath,'w')
        else:
            fout = None
        
        if self.__inpath:
            fin = open(self.__path + '/' + self.__inpath,'r')
        else:
            fin = None
        
        try:
            found_file: bool = False
            for path in (self.__my_path.split(";") + [self.__path]):
                
                command_name = cmd_input[0]
                if os.path.isfile(path + '/' + command_name) and not found_file:
                    found_file = True
                    if ".py" in command_name: 
                        return subprocess.run(["python"] + cmd_input,cwd=path,text=True,stdin=fin,stdout=fout).stdout 
                    elif ".exe" in command_name:
                        return subprocess.run(cmd_input,cwd=path,text=True,stdin=fin,stdout=fout).stdout 
                    return "Unknown command. For additional info type 'help'"
        finally:
            if fout:
                fout.close()
            if fin:
                fin.close()
        if not found_file:
            return ErrorMessage("external",1,command_name).get_msg() #type:ignore
        return ""
    
    
    def main_loop(self):
        while self.__cont:
            user_input = input(f"{self.get_path_str()}>>>")
            print(self.digest_input(user_input))
    
    
    def get_path_str(self):
        return colored("Retyk","green") + colored("@","black") + colored(str(self.__path),"red")


def man(name):
        if name == "dir":
            return "Display content of directory\nUsage - dir <flag> <path> \nDefault Values:\npath = current path \n\nflag explanation --\n-s - recursive"
        elif name == "cd":
            return "Change current directory\nUsage - cd <path>\n\nNo flags supported"
        elif name == "help":
            return "Get help\nUsage - help <command>\nDefault Values:\ncommand = help\n\nNo flags supported"
        elif name == "cat":
            return "Display content of file\nUsage - cat <flag> <path> \n\nflag explanation --\n-n - number output lines"
        elif name == "md":
            return "Make a new directory\nUsage - md <flag> <name> \n\nflag explanation -- \n-c - move to directory"
        elif name == "rm":
            return "Deletes a directory\nUsage - rm <name> \n\nNo flags supported"
        elif name == "exit":
            return "Exits."
        else:
            return "Syntax Error.\nFor additional info type 'help'"

class ErrorMessage():
    __msg: str = ""
    def __init__(self, name :str, code: int, *args) -> None:
        if name == "dir":
            if code == 0:
                self.__msg = "Syntax Error \n" + man("dir")
            elif code == 1:
                self.__msg = f" Directory of {args[0]}\n   File  Not Found"
        
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
                self.__msg = f"File {args[0]} Not Found\n"
        
        elif name == "md":
            if code ==0:
                self.__msg = "Syntax Error \n" + man(name)
        
        elif name == "rm":
            if code == 0:
                self.__msg = "Syntax Error \n" + man(name)
            elif code == 1:
                self.__msg = f"No such directory: {args[0]}\n"
        
        elif name == "set":
            if code == 1:
                self.__msg = f"{args} variable not defined."
            
        elif name == "external":
            if code == 0:
                self.__msg = "Syntax Error\n"
            elif code == 1:
                self.__msg = f"Rerr: File not found: {args[0]}\n"
    
    def get_msg(self) -> str:
        return self.__msg
    
    


def main():
    cmd = CMD()

if __name__ == "__main__":
    main()