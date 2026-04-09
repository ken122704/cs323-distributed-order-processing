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

    if rank == 0:
    # 5-8 orders as required
        orders = [
            {'id': 1, 'item': 'Laptop'}, {'id': 2, 'item': 'Mouse'},
            {'id': 3, 'item': 'Monitor'}, {'id': 4, 'item': 'Keyboard'},
            {'id': 5, 'item': 'Webcam'}, {'id': 6, 'item': 'Headset'}
        ]
    
    print(f"Master: Distributing {len(orders)} orders...")

    for i, order in enumerate(orders):
        # Assign orders to workers (Rank 1 to size-1)
        worker_id = (i % (size - 1)) + 1
        comm.send(order, dest=worker_id)
    
    # Send 'None' to tell workers to stop waiting
    for i in range(1, size):
        comm.send(None, dest=i)
        
    # Setup list to collect results later
    completed_orders = []