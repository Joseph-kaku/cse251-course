"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Joseph Kaku
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.


"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

CPU_COUNT = mp.cpu_count() + 4

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        return f'{value} is prime'
    else:
        return f'{value} not prime'

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt', 'r') as file:
        s_lines = []
        for line in file.readlines():
            s_lines.append(line.strip())
        if word in s_lines:
            return f'{word} found'
        else:
            return f'{word} not found'
            


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f'{text.upper()} uppercase version of {text}'

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    sum = 0
    for i in range(start_value, end_value + 1):
        sum += i
    return f'sum of {start_value:,} to {end_value:,} = {sum:,}'


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{url} has name {data['name']}"
    else:
        f'{url} had an error receiving the information'

#Callback Functions

def callback_task_prime(result):
    result_primes.append(result)

def callback_task_word(result):
    result_words.append(result)
    
def callback_task_upper(result):
    result_upper.append(result)     

def callback_task_sum(result):
    result_sums.append(result)

def callback_task_name(result):
    result_names.append(result)

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools

    prime_task_pool = mp.Pool(3)
    word_task_pool = mp.Pool(1)
    upper_task_pool = mp.Pool(1)
    sum_task_pool = mp.Pool(2)
    name_task_pool = mp.Pool(1)

    # TODO you can change the following
    # TODO start and wait pools
    
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            prime_task_pool.apply_async(task_prime, args=(task['value'], ), callback=callback_task_prime)
            # task_prime(task['value'])
        elif task_type == TYPE_WORD:
            word_task_pool.apply_async(task_word, args=(task['word'], ), callback=callback_task_word)
            # task_word(task['word'])
        elif task_type == TYPE_UPPER:
            upper_task_pool.apply_async(task_upper, args=(task['text'], ), callback=callback_task_upper)
            # task_upper(task['text'])
        elif task_type == TYPE_SUM:
            sum_task_pool.apply_async(task_sum, args=(task['start'], task['end'] ), callback=callback_task_sum)
            # task_sum(task['start'], task['end'])
        elif task_type == TYPE_NAME:
            name_task_pool.apply_async(task_name, args=(task['url'], ), callback=callback_task_name)
            # task_name(task['url'])
        else:
            log.write(f'Error: unknown task type {task_type}')

    print(CPU_COUNT)

    #close all pools
    prime_task_pool.close()
    word_task_pool.close()
    upper_task_pool.close()
    sum_task_pool.close()
    name_task_pool.close()
    
    #join all pools
    prime_task_pool.join()
    word_task_pool.join()
    upper_task_pool.join()
    sum_task_pool.join()
    name_task_pool.join()


    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
