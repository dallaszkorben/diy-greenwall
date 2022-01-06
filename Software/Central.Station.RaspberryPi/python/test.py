#!/usr/bin/python3

import threading

lock = threading.Lock()

def rec(par):

    with lock:

        print(par)
        if par == 3:
            return
        rec(par+1)

rec(1)