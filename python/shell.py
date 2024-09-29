
import os
from termcolor import colored




class ErrorMessage():
    
    __msg: str = ""
    
    def __init__(self, name, code, *args) -> None:
        if name == "dir":
            if code == 0:
                self.__msg = "Syntax Error \n" + self.man("dir")
            elif code == 1:
                self.__msg = f"Directory of {args[0]}\n File  Not Found"

    
    def get_msg(self) -> str:
        return self.__msg
    
    def man(self, name):
        if name == "dir":
            return "Usage - dir <flag> <path> \n flag explantion --"
        


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
    
    
    def digest_input(self,input) -> str:
        
        if len(input) == 0:
            return ""
        fields : list[str] = input.split()
        command = fields[0]
        
        # Internal command (hard coded)
        if command == "dir":
            output = self.dir(fields)
        if command == "exit":
            output = self.exit()
        if command == "help":
            output = self.help()
        if command == "cd":
            output = self.cd(fields)
        if command == "set":
            output = self.set(fields)
        
        return output
    
    
    def dir(self, fields:list[str]):
        if len(fields) == 1:
            return "\n".join(os.listdir("."))
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
            
        # At this point only the dir value is in the list. 
        _dir = fields[0]
        
        if not os.path.isdir(_dir):
            return ErrorMessage("dir", 1, _dir).get_msg()

        return "\n".join(os.listdir(_dir))
        
    def exit(self):
        self.__cont = False
        return "Bye Bye Bye"
    
    def cd(self,directory):
        pass
    
    
    def main_loop(self):
        while self.__cont:
            user_input = input(f"{self.get_path_str()}>>>")
            print(self.digest_input(user_input))
    
    
    def get_path_str(self):
        return colored("Retyk@","green") + colored(str(self.__path),"red")


    
#}
def main():
    cmd = CMD()



if __name__ == "__main__":
    main()





