import threading
import random
import sys


class CircularArrayProcessor:
    def __init__(self, array_size: int, num_rounds: int):
        self.array_size = array_size
        self.num_rounds = num_rounds
        self.array = [random.randint(1, 100) for _ in range(array_size)]
        self.updated_array = self.array.copy()
        self.locks = [threading.Lock() for _ in range(array_size)]
        self.ready_for_round = threading.Event()
        self.current_round = 0
        self.finished_threads = 0

    def _get_neighbors(self, index: int) -> tuple[int, int]:
        left = (index - 1) % self.array_size
        right = (index + 1) % self.array_size
        return left, right

    def _process_element(self, index: int):
        while self.current_round < self.num_rounds:
            self.ready_for_round.wait()

            left_idx, right_idx = self._get_neighbors(index)
            neighbors = [left_idx, index, right_idx]
            neighbors.sort()

            with self.locks[neighbors[0]], self.locks[neighbors[1]], self.locks[neighbors[2]]:
                current_val = self.array[index]
                left_val = self.array[left_idx]
                right_val = self.array[right_idx]

                if current_val < left_val and current_val < right_val:
                    self.updated_array[index] = current_val + 1
                elif current_val > left_val and current_val > right_val:
                    self.updated_array[index] = current_val - 1
                else:
                    self.updated_array[index] = current_val

            with self.locks[0]:
                self.finished_threads += 1
                if self.finished_threads == self.array_size:
                    self.array = self.updated_array.copy()
                    print(self.array)
                    self.finished_threads = 0
                    self.current_round += 1
                    self.ready_for_round.clear()

                    if self.current_round < self.num_rounds:
                        self.ready_for_round.set()

    def run(self):
        print(self.array)

        threads: list[threading.Thread] = []
        for i in range(self.array_size):
            t = threading.Thread(target=self._process_element, args=(i,))
            threads.append(t)
            t.start()

        self.ready_for_round.set()

        for thread in threads:
            thread.join()


def main():
    if len(sys.argv) != 3:
        print("Wrong usage! array_sync.py <array_size> <amount_of_rounds")
    CircularArrayProcessor(15, 5).run()



if __name__ == "__main__":
    main()
