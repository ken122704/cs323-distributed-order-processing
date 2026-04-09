# cs323-distributed-order-processing

## 1. How does the master process distribute tasks to workers?
The master process distributes tasks using **Point-to-Point (P2P) communication** via `mpi4py`'s `comm.send()` method, acting as a central dispatcher rather than broadcasting data globally. To ensure an even distribution of the computational workload across the cluster, it implements a Round-Robin scheduling algorithm, specifically utilizing the modulo operation `(i % (size - 1)) + 1`. This mathematical approach iterates through the generated orders and sequentially assigns discrete tasks to specific worker nodes, maintaining a balanced processing queue across the distributed environment.

---

## 2. What happened when there were more tasks (orders) than workers?
When the system encountered more tasks than available workers, it naturally handled the overflow through task multiplexing and queuing. Because the master utilizes a round-robin approach, workers receive multiple orders in sequence and process them using an infinite `while` loop that acts as a continuous consumer. This means a worker processes its current task, completes it, and immediately receives the next queued task from the master, demonstrating the system's horizontal scalability and its ability to handle large workloads without requiring a strict one-to-one ratio of tasks to CPU cores.

---

## 3. How did the processing delay (`time.sleep`) affect the order of completion?
The simulated processing delay introduced by `time.sleep` resulted in non-deterministic execution, highlighting the asynchronous nature of the system. Because each worker process operates independently on its own timeline, tasks with shorter processing times frequently completed before tasks that were dispatched earlier but required longer processing times. This shows that in a distributed architecture, the chronological order of input does not guarantee the chronological order of output.

---

## 4. What inconsistencies did you observe when running the code without synchronization?
Running the code without synchronization exposed race conditions, leading to data corruption and I/O collisions. When multiple workers attempted to write to shared memory simultaneously, some orders were overwritten or lost, resulting in inaccurate results. Additionally, console outputs overlapped, causing unreadable logs.

---

## 5. How does the shared memory (`multiprocessing.Manager`) help in this activity?
By default, MPI processes operate in separate memory spaces, meaning variables are not shared. The `multiprocessing.Manager()` resolves this by creating a shared memory server process that manages access to a centralized data structure. It provides proxy objects to worker processes and uses Inter-Process Communication (IPC), allowing all processes to safely contribute to shared data.

---

## 6. Explain the importance of using a Lock in a distributed or concurrent system.
A `Lock` (Mutex) is essential for maintaining data integrity in concurrent systems. It ensures that only one process can access shared resources at a time by protecting critical sections of code. Other processes must wait until the lock is released, preventing race conditions and ensuring that operations are executed safely and consistently.