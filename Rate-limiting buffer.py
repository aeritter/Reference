# Made for sending data to a rate-limited API
# Runs in the background, waiting for items to enter the queue.
# Up to X items will be processed every Y seconds.
# New items can be added while it's still processing old ones.
# Uses a threading event to prevent wasting CPU cycles.


import threading, queue, time
lock = threading.Lock()

itemsToAdd = 30             # Number of items to add to the queue (in this example).
sleepTime = 0.15            # Time between each item added to the queue (try 0, 0.05, 0.1, 0.15, and 0.25)
maxItemsPerIteration = 10   # Maximum number of items to pull from the queue at one time.


def lprint(st):
    lock.acquire()
    print(st)
    lock.release()

class backgroundThread(object):
    def __init__(self):
        self.items = queue.Queue()
        self.threadStart = threading.Event()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
        
    def addItem(self, item):
        self.items.put(item)
        
        # Send a pulse to the loop if it's waiting.
        self.threadStart.set()
        self.threadStart.clear()
        
    def loop(self):
        while True:
            lprint("Waiting for pulse.")
            if self.items.qsize() == 0:
                self.threadStart.wait()
            x = 0
            while x < 5:                    
                time.sleep(.2)
                if self.items.qsize() > 0:
                    x = 0
                    try:
                        i = []
                        
                        # Pull up to maxItems from the queue:
                        for y in range(min(self.items.qsize(), maxItemsPerIteration)):
                            i.append(self.items.get())
                            
                        # Do stuff with the items pulled from the queue:
                        lprint(i)
                    except:
                        pass
                    lprint("Waiting 0.2 seconds before next batch of values.")
                
                # increment x so loop can eventually exit so we aren't spinning
                else:
                    x += 1
            lprint("No values in queue for the past second, exiting processing loop.")




bgt = backgroundThread()
time.sleep(1)
lprint("Now adding items to the queue.")
time.sleep(1)
for x in range(itemsToAdd):
    bgt.addItem(x)
    time.sleep(sleepTime)
