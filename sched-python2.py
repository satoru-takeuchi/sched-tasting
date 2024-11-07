#!/usr/bin/python

import sys
import time
import os

NLOOP_FOR_ESTIMATION=100000000
nloop_per_msec = None
progname = sys.argv[0]

def estimate_loops_per_msec():
	before = time.time()
	for _ in range(NLOOP_FOR_ESTIMATION):
		pass
	after = time.time()
	return int(NLOOP_FOR_ESTIMATION/(after-before)/1000)

def child_fn(n):
    progress = 100*[None]
    for i in range(100):
        for _ in range(nloop_per_msec):
            pass
        progress[i] = time.time()

    f = open("%d.data" % (n), "w")
    for i in range(100): 
        f.write("%d\t%d\n" % ((progress[i]-start)*1000, i))
    f.close()
    os._exit(0)

if len(sys.argv) < 2:
    print("usage: ./shced.py <concurrency>")
    sys.exit(1)

concurrency = int(sys.argv[1])

if concurrency < 1:
    print("concurrency must be >= 1")
    sys.exit(1)

nloop_per_msec = estimate_loops_per_msec()

start = time.time()

for i in range(concurrency):
    pid = os.fork()
    if pid < 0:
        sys.exit(1)
    elif pid == 0:
        child_fn(i)

for _ in range(concurrency):
    os.wait()
