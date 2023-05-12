"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Joseph Kaku

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue:Queue251, factory_sem:threading.Semaphore, dealership_sem:threading.Semaphore, lock):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        self.queue = car_queue
        self.factory_sem = factory_sem
        self.dealership_sem = dealership_sem
        self.lock = lock
        


    def run(self):
        for i in range(CARS_TO_PRODUCE):
            self.dealership_sem.acquire() # blocked because full of cars.
            with self.lock:
                car = Car()
                self.queue.put(car)
            self.factory_sem.release() #giving the dealer a car. realease is +1
    
        self.dealership_sem.acquire() # blocked because last full queue
        self.queue.put("no more cars") #signaling that cars are done.   
        self.factory_sem.release() #telling the dealer there are no more cars
        # signal the dealer that there there are not more cars
        


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue:Queue251, dealership_sem:threading.Semaphore, factory_sem:threading.Semaphore, lock):
        self.car_queue = car_queue
        self.dealership_sem = dealership_sem
        self.factory_sem = factory_sem
        self.lock = lock
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        

    def run(self):
        while True:
            self.factory_sem.acquire() #telling dealer to check if there's a spot for a car
            with self.lock:
                car = self.car_queue.get()
                if car == "no more cars":
                    break
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
            self.dealership_sem.release() #Telling factory you need a car
            


def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    
    factory_sem = threading.Semaphore(0)
    dealership_sem = threading.Semaphore(10)
    
    # TODO Create queue251 

    car_queue = Queue251()

    # TODO Create lock(s) ?
    lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    factory = Factory(car_queue, factory_sem, dealership_sem, lock)
    

    # TODO create your one dealership
    dealership = Dealer(car_queue, dealership_sem, factory_sem, lock)

    log.start_timer()

    # TODO Start factory and dealership

    factory.start()
    dealership.start()

    # TODO Wait for factory and dealership to complete
    factory.join()
    dealership.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
