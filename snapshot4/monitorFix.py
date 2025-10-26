# Version 4
import threading
from threading import Lock, Condition
import time

MAX_RESOURCES = 5

class ResourceMonitor:
    def __init__(self, max_resources):
        self.MAX_RESOURCES = max_resources
        self.available_resources = max_resources
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def decreaseCount(self, count):
        with self.condition:
            while self.available_resources < count:
                print(f"Waiting for {count} resources, only {self.available_resources} available.")
                self.condition.wait()
            self.available_resources -= count
            print(f"Acquired {count} resources. There are now {self.available_resources} available.")

    def increaseCount(self, count):
        with self.condition:
            if (self.available_resources + count) <= self.MAX_RESOURCES:
                self.available_resources += count
                print(f"Released {count} resources. There are now {self.available_resources} available resources.")
                self.condition.notify_all()
            else:
                print(f"Error: unable to allocate more than {self.MAX_RESOURCES} resources.")

def workerThread(monitor, threadId):
    print(f"Thread {threadId} starting...")
    monitor.decreaseCount(3)
    time.sleep(0.5)
    monitor.increaseCount(3)
    print(f"Thread {threadId} done.")

def printAvailableResources(monitor):
    print(f"Available resources: {monitor.available_resources}")

def main():
    monitor = ResourceMonitor(5)
    threads = []

    for i in range(3):
        t = threading.Thread(target=workerThread, args=(monitor, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    printAvailableResources(monitor)

if __name__ == "__main__":
    main()
