# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:14:24 2016

@author: Laroy
"""
import Heat.py
from mpi4py import MPI
from numpy import *

comm=MPI_COMM_WORLD
rank=comm.Get_rank()