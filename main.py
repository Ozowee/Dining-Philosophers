import threading
import time
import os
import random
from prettytable import PrettyTable

class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork):
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.eating_count = 0
        self.fork_count = 0
        self.status = "Mysli"

    def run(self):
        while running:
            self.status = "Mysli"
            time.sleep(random.uniform(1,3)) 
            self.status = "Jest Glodny"
            self.dine()

    def dine(self):
        fork1, fork2 = self.left_fork, self.right_fork

        while True:
            fork1.acquire(True)
            self.fork_count = 1
            time.sleep(0.5)  
            locked = fork2.acquire(False)
            if locked: 
                self.fork_count = 2
                break
            fork1.release()
            self.fork_count = 0
            fork1, fork2 = fork2, fork1
        else:
            return

        self.dining()
        fork2.release()
        fork1.release()
        self.fork_count = 0
 
    def dining(self):
        self.status = "Je"
        self.eating_count += 1
        time.sleep(random.uniform(1,3))

def is_locked(lock):
    result = lock.acquire(False)
    if result:
        lock.release()
    return not result

def update_status():
    global philosophers
    table = PrettyTable()
    table.field_names = ["Filozof ID:", "Widelce:", "Status", "Ile razy Jadl"]

    for p in philosophers:
        if p.fork_count == 2:
            forks_display = "| |"
        elif p.fork_count == 1:
            if is_locked(p.left_fork):
                forks_display = "| _"  
            else:
                forks_display = "_ |"
        else:
            forks_display = "_ _"
        table.add_row([p.index, forks_display, p.status, p.eating_count])
    print(table)

def main():
    global running, philosophers
    running = True
    forks = [threading.Lock() for n in range(5)] 
    philosophers = [Philosopher(i, forks[i%5], forks[(i+1)%5]) for i in range(5)]

    for p in philosophers:
        p.start()

    try:
        while running:
            update_status()
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
    except KeyboardInterrupt:
        running = False

    for p in philosophers:
        p.join()

    print("________________")
    for i, p in enumerate(philosophers):
        print(f'Filozof {i} zjadl {p.eating_count} razy.')


if __name__ == "__main__":
    main()