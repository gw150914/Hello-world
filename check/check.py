#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 20:17:59 2022

@author: yuanyong
"""
import time
import numpy as np


a = range(10000000)

#print(np.shape(a))
time.sleep(30)

np.savetxt('a.txt', a)