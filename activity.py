from mpi4py import MPI
import time
import random

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Safety check: Ensure we have enough processes
if size < 2:
    if rank == 0:
        print("Error: Requires at least 2 processes (1 Master, 1 Worker).")
    exit()

if rank == 0:
    print(f"Master Process (Rank {rank}) is online. Total processes: {size}\n")