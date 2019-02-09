# Put whatever you want in this module and do whatever you want with it.
# It exists here as a place where you can "try out" things without harm.

import time
def main(speed,inches):
    start = time.time()
    end = start + inches / speed
    print(start)
    print(end)
    while True:
        t = time.time
        tt=t
        if t >= end:
            print(start)
            print(end)
            break

main(10,100)