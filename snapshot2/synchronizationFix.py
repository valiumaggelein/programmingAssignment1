# Version 2
import threading
from threading import Lock
import time

MAX_RESOURCES = 5
available_resources = MAX_RESOURCES
resource_lock = Lock()

def increaseCount(count):
    global available_resources
    with resource_lock:
        if (available_resources + count) <= MAX_RESOURCES:
            time.sleep(0.001)
            available_resources += count

        else:
            print(f"Error: unable to allocate more than {MAX_RESOURCES} resources")
            return

def decreaseCount(count):
    global available_resources
    with resource_lock:
        if (available_resources - count) >= 0:
            time.sleep(0.001)
            available_resources -= count

        else:
            print("Error: unable to have less than 0 resources")
            return

def printAvailableResources():
    print(f"Available resources: {available_resources}")

def workerThread():
    decreaseCount(2)
    time.sleep(0.001)
    increaseCount(2)
    time.sleep(0.001)
    decreaseCount(4)
    time.sleep(0.001)
    increaseCount(4)

def main():
    threads = []

    for i in range(10):
        t = threading.Thread(target=workerThread)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    printAvailableResources()

if __name__ == "__main__":
    main()
