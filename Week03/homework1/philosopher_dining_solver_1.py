"""
 * Project        Python-Geek-Training
 * (c) copyright  2020
 * Author: Alice Wang

Get the information of top10 movies from Maoyan website
History:
    2020/10/17 initial commit
"""
# problem:
#     https://en.wikipedia.org/wiki/Dining_philosophers_problem
# algorithm:
#     1. chopstick is a shared resource, so it has to be protected by mutex lock
#     2. each philosopher can only eat when he has both left and righ chopstick
#     3. each philosoper, has to lock both left and righ chopstick before eating, if accquiring of any chopstick failed, then waiting
#     4. each philisoper must release both left and righ chopstick after eating
#     5. HIGHLIGH: to avoid deadlock, there are only 4 philosoper allowed sitting on the table

import threading
import os
import time
import random
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)-15s | %(threadName)-8s | %(message)s')
NUM = 5


class Fork():
    def __init__(self, index):
        self.index = index
        self._lock = threading.Lock()

    def pickup(self):
        self._lock.acquire()

    def putdown(self):
        self._lock.release()


class Philosopher( threading.Thread ):
    def __init__(self, index, left_fork, right_fork):
        threading.Thread.__init__( self )
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while True:
            if self.left_fork.index > self.right_fork.index:
                firstFork = self.right_fork
                secondFork = self.left_fork
            else:
                firstFork = self.left_fork
                secondFork = self.right_fork
            firstFork.pickup()
            secondFork.pickup()
            self.eating()

            secondFork.putdown()
            firstFork.putdown()
            self.thinking()

    def eating(self):
        logging.info(f'Philosopher {self.index} starts to eat' )
        time.sleep( random.choice( [1, 2] ) )
        logging.info( f'Philosopher {self.index} finishes eating' )

    def thinking(self):
        logging.info( f'Philosopher {self.index} is thinking' )
        time.sleep( random.choice( [1, 2] ) )


if __name__ == '__main__':
    forks = [Fork( i ) for i in range( NUM )]
    philosophers = [Philosopher( i, forks[i], forks[(i + 1) % NUM] ) for i in range( NUM )]

    for p in philosophers:
        p.start()
    for p in philosophers:
        p.join()
