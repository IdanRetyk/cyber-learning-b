import os,re,subprocess,random
from termcolor import colored


class CMD():
    # Singleton
    def __init__(self):
        self.__outpath: str = ""
        self.__inpath: str = ""
        self.__path: str = os.getcwd().replace('\\','/') # Any os will use forward slash (windows supports )
        self.__cont: bool = True
        self.__my_path: str = os.environ["PATH"] + "/Users/Idan/cyber-learning-b/python;/Users/Idan/downloads;"
        
        self.interals: list[str] = ["dir","exit","help","cd","set","cat","md","rm"]
        self.cmd_comands: list[str] = ["copy","ren","echo"]
        
        self.bootloader()
        
        self.main_loop()
        

    def bootloader(self):
        print("Retyk's shell [Version 1.0]\n(c) Herzog Corporation. All rights reserved.")
        print()
    
    
    def digest_input(self,input: str, pipe: int = 0) -> str :
        
        if len(input) == 0:
            return ""
        outpath,inpath = "",""
        if '|' in input:
            first,second = input.split('| ')
            return (self.handle_pipe(first,second))
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
            return self.run_external(fields,pipe)
            
        
        if outpath: # if output is redirected
            with open(self.__path + '/' + outpath,'w') as file:
                file.write(output)
            return ""
        else:
            return output
    
    def handle_pipe(self,first :str,second: str) -> str:
        # If first command is internal simply call digest input twice.
        if first.split()[0] in self.interals: 
            file_name = str(random.randint(1000,9999)) + '.txt'
            while os.path.isfile(self.__path + '/' + file_name):
                file_name = str(random.randint(1000,9999)) + '.txt'
            self.digest_input(f"{first} > {file_name}")
            output = self.digest_input(f"{second} < {file_name}")
            os.remove(self.__path + '/' + file_name)
            return output
        
        # If second command is internal, perform the first command without any output, and than the second one as usual
                            #as none of the internal commands support input redirect.
        if second.split()[0] in self.interals: 
            self.digest_input(f"{first}")
            return self.digest_input(f"{second}")
        
        
        # If both are external actually handle pipe.
        
        err_msg1 = self.digest_input(first,1)
        err_msg2 = self.digest_input(second,2)
        if err_msg1 or err_msg2:
            return err_msg2 + err_msg1
        p1,p2 = self.p1,self.p2
        p1.stdout.close() # type:ignore
        print("Before communicate")
        try:
            outs, errs = p2.communicate() # type:ignore
            print("After Communicate")
            if outs:
                print(outs)
            return ""

        except subprocess.TimeoutExpired:
            p2.kill() # type:ignore
            outs, errs = p2.communicate() # type:ignore
            return ""
        
        
    
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
            return self.__path +'\n'
        if len(args) == 2:
            path = args[1]
        else:
            return ErrorMessage("cd", 0).get_msg()
        
        if os.path.isabs(path): # Absolute path was given
            self.__path = path.replace("\\",'/')
            return ""
        # Relative path
        
        init_path = self.__path # Backup path incase one of the directories doesn't exist
        
        for directory in path.split("/"):
            
            if directory == '.': # Path is the same
                pass
            elif directory == "..": # Backtrack one directory
                if re.search("[a-z]:/.+",self.__path.lower()): # If there is only one directory left, don't backtrack.
                    self.__path = "/".join(self.__path.split("/")[:-1])
            else:
                if os.path.isdir(self.__path + "/" + directory):
                    self.__path += '/'
                    self.__path += directory
                    self.__path.replace('\\','/')
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

        
        if os.path.exists(self.__path +'/' + name):
            return ErrorMessage("md",1,name).get_msg()
        
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
            
    def run_external(self,cmd_input: list[str], pipe:int = 0) ->  str:
        if len(cmd_input) == 0:
            return ErrorMessage("external",0).get_msg()
        
        if not pipe:
            if self.__outpath:
                fout = open(self.__path + '/' + self.__outpath,'w')
            else:
                fout = None
            
            if self.__inpath:
                fin = open(self.__path + '/' + self.__inpath,'r')
            else:
                fin = None
        else:
            if pipe == 1:
                fout = subprocess.PIPE
                if self.__inpath:
                    fin = open(self.__path + '/' + self.__inpath,'r')
                else:
                    fin = None
            else:
                if self.__outpath:
                    fout = open(self.__path + '/' + self.__outpath,'w')
                else:
                    fout = None
                fin = self.p1.stdout # type:ignore
        
        try:
            found_file: bool = False
            
            proc = ""
            command_name = cmd_input[0]
            if ".py" in command_name: # If python file, look in hardcoded path for the file.
                for path in (self.__my_path.split(";") + [self.__path]):
                    if os.path.isfile(path + '/' + command_name) and not found_file:
                        found_file = True 
                        proc = subprocess.Popen(["python"] + cmd_input,cwd=path,text=True,stdin=fin,stdout=fout)
                        
                if not found_file:
                    return f"File not found: {command_name}"
            else:
                if command_name in self.cmd_comands: # If external for the shell but interal for actual cmd.
                    proc = subprocess.Popen(["cmd.exe","/c"] + cmd_input,cwd=self.__path,text=True,stdin=fin,stdout=fout)
                else:
                    proc =  subprocess.Popen(cmd_input,cwd=self.__path,text=True,stdin=fin,stdout=fout)
                
            
            if pipe == 1:
                self.p1 = proc
            elif pipe == 2:
                self.p2 = proc
            else:
                proc.wait() #type:ignore
            return ""
        finally: # If fout and fin are files make sure to close them no matter what happened to the script.
            if fout and not isinstance(fout,int):
                fout.close()
            if fin and not isinstance(fin,int):
                fin.close()

    
    def main_loop(self):
        while self.__cont:
            user_input = input(f"{self.get_path_str()}>>>")
            print(self.digest_input(user_input))
    
    
    def get_path_str(self):
        return colored("Retyk","green") + colored("@","black") + colored(str(self.__path),"red")



def man(name):
        if name == "dir":
            return "Display content of directory\nUsage - dir <flag> <path> \nDefault Values:\npath = current path \n\nflag explanation --\n-s - recursive\n"
        elif name == "cd":
            return "Change current directory\nUsage - cd <path>\n\nNo flags supported\n"
        elif name == "help":
            return "Get help\nUsage - help <command>\nDefault Values:\nif not command give, explain about the script\n\nNo flags supported\n"
        elif name == "cat":
            return "Display content of file\nUsage - cat <flag> <path> \n\nflag explanation --\n-n - number output lines\n"
        elif name == "md":
            return "Make a new directory\nUsage - md <flag> <name> \n\nflag explanation -- \n-c - move to directory\n"
        elif name == "rm":
            return "Deletes a directory\nUsage - rm <name> \n\nNo flags supported\n"
        elif name == "exit":
            return "Exits.\n"
        else:
            return "Syntax Error.\nFor additional info type 'help'\n"

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
            elif code == 1:
                self.__msg = f"Directory already exist: {args[0]}"
        
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