"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Joseph Kaku

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

I am going to use threads for each fork that comes up in a path. THis will happen until there 
is an end found. 

Why would it work?

This will work because all possible paths will be explored getting to the end of the maze faster

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def solve_path(maze, start, color, path_found, lock):

    global thread_count
    threads = list()
    (row_start,col_start) = start

    while True:
        if not maze.can_move_here(row_start,col_start) or path_found[0]:
            join_threads = list([i for i in threads])
            for i in join_threads:
                i.join() 
            return

        
        with lock:
            maze.move(row_start,col_start, color)
        
        possible_moves = maze.get_possible_moves(row_start,col_start)
       
        if len(possible_moves) == 0:
            
            if not maze.at_end(row_start,col_start):
                
                join_threads = list([i for i in threads])
                for i in join_threads:
                    i.join() 
                return
                
            path_found[0] = True
        
        else:
            if len(possible_moves) > 1:
                new_threads = list()
                colr = get_color()
                
                for i in range(len(possible_moves) - 1):
                    
                    thread_count+=1
                    
                    new_threads.append(threading.Thread(target = solve_path, args =
                        (maze, possible_moves[i],colr , path_found, lock))) 
                
                threads.extend(new_threads)

                for thread in new_threads:
                    thread.start() 
                (row_start, col_start) = possible_moves[-1]
            else:
                (row_start, col_start) = possible_moves[0]



def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
   
    global thread_count
    
    path_solved = list([False])
    
    start_position = maze.get_start_pos()
    
    color = get_color()
   
    lock = threading.Lock()
    
    begin_thread = threading.Thread(target = solve_path,
        args = (maze, start_position, color, path_solved, lock))
   
    threads = list([begin_thread])
    thread_count+=1

    for i  in threads:
        i.start()
    for i in threads:
        i.join()


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()