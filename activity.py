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
    
        orders = [
            {'id': 1, 'item': 'Laptop'}, {'id': 2, 'item': 'Mouse'},
            {'id': 3, 'item': 'Monitor'}, {'id': 4, 'item': 'Keyboard'},
            {'id': 5, 'item': 'Webcam'}, {'id': 6, 'item': 'Headset'}
        ]
    
    print(f"Master: Distributing {len(orders)} orders...")

    for i, order in enumerate(orders):
        
        worker_id = (i % (size - 1)) + 1
        comm.send(order, dest=worker_id)
    
    
    for i in range(1, size):
        comm.send(None, dest=i)
        
    
    completed_orders = []

else:
    while True:
        order = comm.recv(source=0)
        if order is None: 
            break
            
        print(f"  [Worker {rank}] Processing Order {order['id']} ({order['item']})...")
        
        time.sleep(random.uniform(1, 3))

comm.send(order, dest=0)
print(f"  [Worker {rank}] Order {order['id']} sent back to Master.")

if rank == 0:
    print("\nMaster is waiting to collect completed orders...")
    for _ in range(len(orders)):
        finished_task = comm.recv(source=MPI.ANY_SOURCE)
        completed_orders.append(finished_task)

        comm.send(order, dest=0)
        print(f"  [Worker {rank}] Order {order['id']} sent back to Master.")

if rank == 0:
    print("\nMaster is waiting to collect completed orders...")
    for _ in range(len(orders)):
        finished_task = comm.recv(source=MPI.ANY_SOURCE)
        completed_orders.append(finished_task)


comm.Barrier()

if rank == 0:
    print("\n--- Final Processed Order List ---")
    for task in completed_orders:
        print(f"Completed: {task['item']} (ID: {task['id']})")