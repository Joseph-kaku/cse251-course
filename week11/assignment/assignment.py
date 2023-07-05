"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(id, startTime, cleanerLock, cleanedCount):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while True:
        if time.time() - startTime >= TIME:
            break

        cleaner_waiting()
        cleanerLock.acquire()
        print(STARTING_CLEANING_MESSAGE)
        cleanedCount.value = cleanedCount.value + 1
        cleaner_cleaning(id)
        print(STOPPING_CLEANING_MESSAGE)
        cleanerLock.release()


def guest(id, guestLock, startTime, cleanerLock, partyCount, countInRoom):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while True:
        if time.time() - startTime >= TIME:
            break
        guest_waiting()
        guestLock.acquire()
        countInRoom.value = countInRoom.value + 1
        if countInRoom.value == 1:
            cleanerLock.acquire()
            print(STARTING_PARTY_MESSAGE)
            partyCount.value = partyCount.value + 1
        guestLock.release()

        guest_partying(id, countInRoom.value)
        guestLock.acquire()
        countInRoom.value = countInRoom.value - 1
        if countInRoom.value == 0:
            print(STOPPING_PARTY_MESSAGE)
            cleanerLock.release()
        guestLock.release()

def main():
    # Start time of the running of the program. 
    startTime = time.time()

    # TODO - add any variables, data structures, processes you need
    cleanerLock = mp.Manager().Lock()

    guestLock = mp.Manager().Lock()

    cleanedCount = mp.Manager().Value('i', 0)

    partyCount = mp.Manager().Value('i', 0)

    countInRoom = mp.Manager().Value('i', 0)

    # TODO - add any arguments to cleaner() and guest() that you need
    cleaners, guests = list(),list()

    for i in range(CLEANING_STAFF):
        cleaners += [mp.Process(target=cleaner, args=(i+1,startTime, cleanerLock, cleanedCount))]

    for i in range(HOTEL_GUESTS):
        guests += [mp.Process(target=guest, args=(i+1, guestLock, startTime, cleanerLock, partyCount, countInRoom))]

    #processes start
    for i in guests:
        i.start()
    for j in cleaners:
        j.start()

    #processes end
    for i in guests:
        i.join()
    for j in cleaners:
        j.join()

    # Results
    print(f'Room was cleaned {cleanedCount.value} times, there were {partyCount.value} parties')


if __name__ == '__main__':
    main()

