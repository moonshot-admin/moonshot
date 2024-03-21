import os
import asyncio
from typing import TypeVar
from typing import Callable
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process

from ....services.base_service import BaseService
from ..interface.queue_connection import InterfaceQueueConnection

T = TypeVar("T")

class InMemoryQueue(InterfaceQueueConnection[T], BaseService):
    executor: ProcessPoolExecutor | None
    queue_monitor: Process
    queue: asyncio.Queue[T]
    queue_name: str
    monitor_started: bool

    def __init__(self, queue_name: str):
        super().__init__()
        self.name = queue_name
        self.queue = asyncio.Queue()
        self.workers: list[Callable[[T], None]] = []
        self.monitor_started = False
        self.executor = None
        self.queue_name = ''
    
    async def monitor_queue(self):
        if self.monitor_started:
            return
        self.logger.debug(f" {self.queue_name} - monitor loop started")
        self.logger.debug(f" Process ID: {os.getpid()}")
        self.monitor_started = True
        try:
            while True:
                try:
                    job = await self.queue.get()  # do not use get_nowait, to avoid busy waiting
                    loop = asyncio.get_running_loop()
                    for worker in self.workers:
                        await loop.run_in_executor(self.executor, worker, job)
                except asyncio.QueueEmpty:
                    await asyncio.sleep(1) # Sleep for a bit to avoid busy waiting
                except Exception as e:
                    self.logger.error(f"[error] - monitor_queue: {e}")
                    break
        except Exception as e:
            self.logger.error(f"[error] - monitor_queue: {e}")

    def connect(self, queue_name: str | None = None) -> InterfaceQueueConnection[T]:
        # this is an in-memory queue, there's no external connection to establish.
        return self

    def subscribe(self, worker: Callable[[T], None]) -> None:
        self.workers.append(worker)
        if not self.executor or not self.queue_monitor.is_alive():
            self.executor = ProcessPoolExecutor(4)
        if not hasattr(self, 'queue_monitor') or not self.queue_monitor.is_alive():
            # Define a wrapper function to run the asyncio event loop and the monitor_queue coroutine
            def start_monitor_queue():
                asyncio.run(self.monitor_queue())

            monitor_queue_process = Process(target=start_monitor_queue, args=(self, worker))
            monitor_queue_process.daemon = False
            monitor_queue_process.start()
            self.queue_monitor = monitor_queue_process

    def unsubscribe(self) -> None:
        if self.queue_monitor.is_alive():
            self.queue_monitor.terminate()
            self.queue_monitor.join()
        if self.executor:
            self.executor.shutdown(wait=True)

    def publish(self, task: T) -> bool:
        try:
            self.queue.put_nowait(task)
            self.logger.debug(f"Published task {task} to queue {self.queue_name} - {self.queue.qsize()}")
            return True
        except:
            return False

    def close(self):
        # just clear the queue to mimic closing connection.
        while not self.queue.empty():
            self.queue.get_nowait()
