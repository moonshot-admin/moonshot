import concurrent.futures
import multiprocessing
import asyncio
import time
import uuid
import os

class BenchmarkProcessPoolExecutor(concurrent.futures.Executor):
    def __init__(self, max_workers=4):
        self.tasks_queue = multiprocessing.Queue()
        self.processes = []
        self.task_status = {}

        for _ in range(max_workers):
            p = multiprocessing.Process(target=self.worker)
            p.start()
            self.processes.append(p)

    def worker(self):
        while True:
            task_id, fn, args, kwargs = self.tasks_queue.get()
            if task_id is None:  # Shutdown signal
                break
            try:
                fn(*args, **kwargs)
                self.task_status[task_id] = 'completed'
            except Exception as e:
                self.task_status[task_id] = f'failed: {e}'

    def submit(self, fn, *args, **kwargs):
        task_id = uuid.uuid4()
        self.tasks_queue.put((task_id, fn, args, kwargs))
        self.task_status[task_id] = 'pending'
        return task_id

    def shutdown(self, wait=True):
        # Send shutdown signal to each worker
        for _ in self.processes:
            self.tasks_queue.put((None, None, None, None))

        # Optionally wait for workers to finish
        if wait:
            for p in self.processes:
                p.join()

        # Clear queue and processes
        while not self.tasks_queue.empty():
            self.tasks_queue.get()
        self.processes = []

def blocking_function(task_num):
    for i in range(5):
        print(f"Task {task_num}, Process {os.getpid()}, working... {i}")
        time.sleep(1)

async def run_blocking_function(executor):
    # Submit multiple tasks to the executor
    task_ids = [executor.submit(blocking_function, i) for i in range(10)]

    # Wait a bit for tasks to complete
    await asyncio.sleep(10)

    # Shutdown the executor
    executor.shutdown()

async def main():
    executor = CustomProcessPoolExecutor(max_workers=4)
    await run_blocking_function(executor)