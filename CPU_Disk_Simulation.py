import sys
from queue import PriorityQueue, Queue
import random
import math

#uniform_dist returns float between 0 and 1. larger max_value = finer grain floats
def uniform_dist(max_value: int):
    rand_int = random.randint(0,max_value)
    return (rand_int / max_value + 0.0000000001)   

#exponential dist takes in service time and returns an exponentially distributed float
def exponential_dist(t: float):
    uni_float = uniform_dist(10000000)
    return -t*math.log(uni_float)

#Event class stores information about event type and time
#event_time used to order in priority queue. (order of "execution")
class Event():
    def __init__(self, type: str, event_time: float):
        self.type = type
        self.event_time = event_time

#Process class stores information about processes.
#Instances added to readyQ for CPU and diskQ for disk
class Process():
    processID = 0 #ProcessID is unneeded/used, but mentioned in assignments.

    def __init__(self):
        self.processID = Process.processID
        Process.processID += 1
        self.waiting_time = 0
        self.service_time = 0

#Simulation class handles the running of the workload simulation.
class Simulation():
    #initializing simulation upon construction of instance
    #takes in service rate, cpu service time, and disk service time
    def __init__(self, arrival_rate, CPUServiceTime, DiskServiceTime):
        self.arrival_rate: float = arrival_rate #technically will only be an int, but either is fine.
        self.CPUServiceTime: float = CPUServiceTime
        self.DiskServiceTime: float = DiskServiceTime
        self.clock: float = 0
        self.is_server_idle: bool = True
        self.totalTurnaround: float = 0
        self.completedProcesses: int = 0
        self.weightedProcessInReadyQ: float = 0
        self.busyTime: float = 0
        self.eventQ = PriorityQueue()
        self.readyQ = Queue()
        self.diskQ = Queue()


        #Adding single arrival event to queue
        self.ScheduleEvent("cpu_arr", exponential_dist(float(1/self.arrival_rate)))
    
    def ScheduleEvent(self, type: str, event_time: float):
        event = Event(type, event_time)
        self.eventQ.put((event_time,event)) #FIXME why add an event if you're just going to make it a tuple with time anyways?

    def Run(self):
        while self.completedProcesses != 10000:
            e = self.eventQ.get()[1]
            old_clock = self.clock
            clock = e.event_time #updating clock to time that event occurs
            if e.type == "cpu_arr":
                return #FIXME
            elif e.type == "cpu_dep":
                return #FIXME
            elif e.type == "disk_arr":
                return #FIXME
            elif e.type == "disk_dep":
                return #FIXME
    

    @classmethod
    def from_command_line(cls):
        if len(sys.argv) <= 3:
            print("To run the simulation, call the script with the following arguments:\n" \
                    "Argument 1: Arrival rate (λ) in processes per second\n" \
                    "Argument 2: CPU Service Time in seconds\n" \
                    "Argument 3: Disk Service Time in seconds\n" \
                    "i.e. python CPU_Disk_Simulation.py <arrival rate> <CPU service time> <disk service time>")
            sys.exit()
        
        return cls(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    
if __name__ == "__main__":
    sim = Simulation.from_command_line()
    sim.Run()    