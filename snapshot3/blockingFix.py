# Version 3
import threading
from threading import Lock, Condition
import time

MAX_RESOURCES = 5
available_resources = MAX_RESOURCES
resource_lock = Lock()
resource_condition = Condition(resource_lock)

def increaseCount(count):
    global available_resources
    with resource_condition:
        if (available_resources + count) <= MAX_RESOURCES:
            available_resources += count
            print(f"Released {count} resources. There are now {available_resources} available resources.")
            resource_condition.notify_all()
        else:
            print(f"Error: unable to allocate more than {MAX_RESOURCES} resources.")
            return

def decreaseCount(count):
    global available_resources
    with resource_condition:
        while available_resources < count:
            print(f"Waiting for {count} resources, only {available_resources} available.")
            resource_condition.wait()


        available_resources -= count
        print(f"Acquired {count} resources. There are now {available_resources} resources available.")

def printAvailableResources():
    print(f"Available resources: {available_resources}")

def workerThread(threadId):
    print(f"Thread {threadId} starting...")
    decreaseCount(3)
    time.sleep(0.5)
    increaseCount(3)
    print(f"Thread {threadId} done.")

def main():
    threads = []

    for i in range(5):
        t = threading.Thread(target=workerThread, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    printAvailableResources()

if __name__ == "__main__":
    main()
