"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Joseph Kaku
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, marble_giv, marbles_to_create, creator_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.marbles_to_create = marbles_to_create
        self.sender = marble_giv
        self.delay = creator_delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marbles_to_create):
            self.sender.send(random.choice(Marble_Creator.colors))
            time.sleep(self.delay)
        self.sender.send('fin')
        self.sender.close()
        print('\nCREATOR FINISHED\n')


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, marble_get, bagger_giv, bagger_delay, count_in_bag):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.receiver = marble_get
        self.sender = bagger_giv
        self.delay = bagger_delay
        self.count_in_bag = count_in_bag

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        marbles_bagged = list()
        while True:
            # get marbles from pipe
            value = self.receiver.recv() 
            if value == 'fin':
                break
            marbles_bagged.append(value)
            if len(marbles_bagged) == self.count_in_bag:
                self.sender.send(marbles_bagged)
                marbles_bagged.clear()
            time.sleep(self.delay)

        self.sender.send('fin')
        self.receiver.close()
        self.sender.close()
        print('\nBAGGER FINISHED\n')


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, bagger_get, assemble_giv, assembler_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.receiver = bagger_get
        self.sender = assemble_giv
        self.delay = assembler_delay

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            value = self.receiver.recv()
            if value == 'fin':
                break
            value.append(random.choice(Assembler.marble_names))
            self.sender.send(value)
            time.sleep(self.delay)

        self.sender.send('fin')
        self.receiver.close()
        self.sender.close()
        print('\nBAGGER FINISHED\n')


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, assembler_get, filename, wrapper_delay, shared_counter):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.receiver = assembler_get
        self.filename = filename
        self.delay = wrapper_delay
        self.shared_counter = shared_counter
        self.gift_counter = 0

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.filename, 'w') as f:
            while True:
                value = self.receiver.recv()
                if value == 'fin':
                    break

                f.write('Created - ' + str(datetime.now().time()) + ': Large marble: ')
                f.write(value.pop()+', marbles: ')
                for x in value:
                    f.write(x + ', ')
                f.write('\n\r')
                self.gift_counter += 1
                time.sleep(self.delay)
        self.receiver.close()
        self.shared_counter[0] += self.gift_counter 
        print('\nWRAPPER FINISHED\n')



def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    marble_giv, marble_get = mp.Pipe()
    bagger_giv, bagger_get = mp.Pipe()
    assemble_giv, assemble_get = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    gift_counter = mp.Manager().list([0])

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creator = Marble_Creator(marble_giv, settings['marble-count'], settings['creator-delay'])
    bagger = Bagger(marble_get, bagger_giv, settings['bagger-delay'], settings['bag-count'])
    assembler = Assembler(bagger_get, assemble_giv, settings['assembler-delay'])
    wrapper = Wrapper(assemble_get, BOXES_FILENAME, settings['wrapper-delay'], gift_counter)

    log.write('Starting the processes')
    # TODO add code here
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(f'\t{gift_counter[0]} gifts were created')



if __name__ == '__main__':
    main()

