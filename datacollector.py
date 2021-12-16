from threading import Thread
import statistics, time

class DataCollector(Thread):
    def __init__(self, fetch_function, cycle_time = 1, store_cycles = 30):
        self.fetch_function = fetch_function
        self.cycle_time = cycle_time
        self.store_cycles = store_cycles
        self.stopped = False

        self.values = [fetch_function()]
        Thread.__init__(self)

    @property
    def average(self):
        return statistics.mean(self.values)

    def run(self):
        while not self.stopped:
            self.values.append(self.fetch_function())

            if len(self.values) > self.store_cycles:
                self.values = self.values[1:]

            time.sleep(self.cycle_time)

    def stop(self):
        self.stopped = True
