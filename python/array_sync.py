import threading
from random import randint




def synchronize_array(n: int, m: int):
    events: list[threading.Event] = [threading.Event() for _ in range(n)]
    locks: list[threading.Lock] = [threading.Lock() for _ in range(n)]
    
    array: list[int] = [randint(1,100) for _ in range(n)]
    print("initial array: ", array)


def main() -> None:
    synchronize_array(15, 5)

if __name__ == "__main__":
    main()
