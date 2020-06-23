import os
import psutil
import multiprocessing, threading
import numpy

def heavy_computation(data_chunk):
    matrix_A, matrix_B = data_chunk
    matrix_C = [[0 for i in range(len(matrix_B[0]))] for i in range(len(matrix_A))]

    for i in range(len(matrix_A)):
        for j in range(len(matrix_B[0])):
            el = 0
            for k in range(len(matrix_A[0])):
                el += matrix_A[i][k] * matrix_B[k][j]

            matrix_C[i][j] = el

    return matrix_C

class ProcessPool():
    def __init__(self, min_workers, max_workers, mem_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = self.mem_usage
        self.workers = []

        self.task_queue = multiprocessing.Queue()
        self.res_queue = multiprocessing.Queue()

        self.psutil = psutil.Process(os.getpid())

        self.estimated_workers = False
        self.max_worker_usage = 0
        #создание проессов
        self.monitor_worker = threading.Thread(target=self.memory, args=())

        self.running = False
    # Следим за памятью
    def memory(self):
        while self.running:
            sum_memory = 0

            for work in self.workers:
                if work.is_alive:
                    try:
                        pr = psutil.Process(work.pid)
                        worker_usage_mem = pr.memory_info().rss
                    except Exception as e:
                        pass
                    sum_memory += worker_usage_mem

            if not self.estimated_workers:
                self.max_worker_usage = max(sum_memory, self.max_worker_usage)
            else:
                for work in self.workers:
                    if (not work.is_alive) and sum_memory + self.max_worker_usage <= self.mem_usage:
                        sum_memory += self.max_worker_usage
                        work.start()
                #остановка процесса

                while sum_memory > self.mem_usage:
                    for work in self.workers:
                        if work.is_alive:
                            pr = psutil.Process(work.pid)
                            worker_usage_mem = pr.memory_info().rss

                            if worker_usage_mem >= self.mem_usage / len(self.workers):
                                sum_memory -= worker_usage_mem
                                work.terminate()

                        if sum_memory < self.mem_usage:
                            break

    def process_function(self, function):
        while True:
            task = self.task_queue.get()
            res = function(task)
            self.res_queue.put_nowait(res)
            if not self.estimated_workers:
                break
    # test
    def zero_workers(self, function, example):
        zero = multiprocessing.Process(
            target=self.process_function,
            args=(function,),
            name="ZERO process",
        )

        self.workers.append(zero)
        zero.start()

        self.task_queue.put(example)

        while self.res_queue.empty():
            continue
        else:
            res = self.res_queue.get()

            self.estimated_workers = True
            self.max_workers = min(self.max_workers, self.mem_usage // self.max_worker_usage)

            zero.terminate()
            self.workers.clear()

            return res
    # запуск процессов
    def start(self):
        self.running = True
        self.monitor_worker.start()
    # инициализация воркеров
    def initial_workers(self, function):
        for i in range(0, self.max_workers):
            w = multiprocessing.Process(
                target=self.process_function,
                args=(function,)
            )

            self.workers.append(w)

        for w in self.workers:
            w.start()

    def end(self):
        for w in self.workers:
            w.terminate()

        self.running = False
        self.workers.clear()

    def map(self, function, big_data):
        self.start()

        comparatives_result = [self.zero_workers(function, big_data.pop(0))]

        self.initial_workers(function)

        for data in big_data:
            self.task_queue.put(data)

        for i in range(len(big_data)):
            comparatives_result.append(self.res_queue.get())

        self.end()

        return comparatives_result


if __name__ == '__main__':
    pool = ProcessPool(min_workers=2, max_workers=10, mem_usage='1Gb')
    big_data = [(numpy.random.randn(999, 999), numpy.razndom.randn(999, 999)) for i in range(10)]
    result = pool.map(heavy_computation, big_data)

