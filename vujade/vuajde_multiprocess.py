"""
Dveloper: Sungjun Yoon
E-mail: sjyoon1671@gmail.com
Github: https://github.com/vujadeyoon
Date: May 31, 2020.

Title: vujade_multiprocess.py
Version: 0.1
Description: Multi-process module
"""


import os
import time
from multiprocessing import Process
from multiprocessing import Queue


class _BaseMultiProcess:
    def __init__(self, _target_method, _num_proc=os.cpu_count()):
        self.target_method = _target_method
        self.num_proc = _num_proc

    def _proc_setup(self):
        self.queue = Queue()
        self.process = [Process(target=self.target_method, args=(self.queue,)) for _ in range(self.num_proc)]

        for p in self.process: p.start()

    def _proc_release(self):
        for _ in range(self.num_proc): self.queue.put((None, None)) # Todo: The number of parameters for queue.put() should be checked.
        while not self.queue.empty(): time.sleep(1)
        for p in self.process: p.join()
