"""
Dveloper: Sungjun Yoon
E-mail: sjyoon1671@gmail.com
Github: https://github.com/vujadeyoon
Date: May 31, 2020.

Title: vujade_utils.py
Version: 0.1
Description: Useful utils
"""


import time
import argparse


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class avgmeter_time:
    def __init__(self, _num_batch=1):
        self.num_batch = _num_batch
        self.eps_val = 1e-9
        self.time_rec = []
        self.time_len = self.time_rec.__len__()
        self.time_total = 0.0
        self.time_avg = 0.0
        self.fps_total = 1 / (self.time_total + self.eps_val)
        self.fps_avg = 1 / (self.time_avg + self.eps_val)

    def tic(self):
        self.time_start = time.time()

    def toc(self):
        self.time_rec.append(time.time() - self.time_start)
        self.__update()

    def __update(self):
        self.time_len = self.time_rec.__len__()
        self.time_total = sum(self.time_rec)
        self.time_avg = sum(self.time_rec) / (self.num_batch * self.time_len)
        self.fps_total = 1 / (self.time_total + self.eps_val)
        self.fps_avg = 1 / (self.time_avg + self.eps_val)
