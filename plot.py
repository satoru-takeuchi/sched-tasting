#!/usr/bin/python3

import sys
import time
import os
import plot_sched

concurrency = int(sys.argv[1])

plot_sched.plot_sched(concurrency)
