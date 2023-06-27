"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Joseph Kaku

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""

from multiprocessing import shared_memory
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2


def write(writeSem, readSem, lock, sharedList):
    while True:
      writeSem.acquire()

      with lock:
        if sharedList[12] and sharedList[13]:
          sharedList[13] == 1
          break

        index = sharedList[11] % BUFFER_SIZE
        sharedList[index] = sharedList[12] + 1
        sharedList[11] = index + 1
        sharedList[12] += 1

      readSem.release()
      readSem.release()


def read(readSem, writeSem, lock, sharedList):
    while True:
      readSem.acquire()

      with lock:
          if (sharedList[13] and sharedList[10] == sharedList[11]):
             break
          
          index = sharedList[10] % BUFFER_SIZE
          print(sharedList[index], end=', ', flush= True)
          sharedList[10] = index + 1
          sharedList[13] += 1

      writeSem.release()



def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))

    #                         10    11      12        13        14
    # [0,1,2,3,4,5,6,7,8,9, FRONT, BACK, recvCOUNT, MakeNum, isDone]


    sharedlist = smm.ShareableList([0]*14)
    sharedlist[13] = items_to_send

    # sharedlist[10] = 0
    # sharedlist[11] = 0
    # sharedlist[12] = 1
    # sharedlist[13] = items_to_send

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    lock = mp.Lock()
    readSem = mp.Semaphore(10)
    writeSem = mp.Semaphore(10)

    # TODO - create reader and writer processes
    readProcess = mp.Process(target=read, args=(readSem, writeSem, lock, sharedlist))
    writeProcess = mp.Process(target=write, args=(readSem, writeSem, lock, sharedlist))

    # TODO - Start the processes and wait for them to finish
     
    readProcess.start()
    writeProcess.start()

    readProcess.join()
    writeProcess.join()


    print(f'{items_to_send} values sent')
    print(f'{sharedlist[13]} values received')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
