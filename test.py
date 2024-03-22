
def new_add(self:int, other:str) -> str:
    return int(other) + self
    


int.__add__ = new_add

print(int.__add__(1,1))