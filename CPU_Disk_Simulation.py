import sys
from queue import PriorityQueue, Queue
import random
import math

#uniform_dist returns float between 0 and 1. larger max_value = finer grain floats
def uniform_dist(max_value):
    rand_int = random.randint(0,max_value)
    return (rand_int / max_value + 0.0000000001)   

#exponential dist takes in service time and returns an exponentially distributed float
def exponential_dist(self, t):
    uni_float = self.uniform_dist(10000000)
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
    def __init__(self, lamb, CPUServiceTime, DiskServiceTime):
        self.clock = 0
        self.serverIdle = True
        self.totalTurnaround = 0
        self.completedProcesses = 0
        self.weightedProcesInReadyQ = 0
        self.busyTime = 0
        self.eventQ = PriorityQueue()
        self.readyQ = Queue()
        self.diskQ = Queue()
        self.lamb = lamb
        self.CPUServiceTime = CPUServiceTime
        self.DiskServiceTime = DiskServiceTime

        #Adding single arrival event to queue
        self.ScheduleEvent("cpu_arr", self.clock + exponential_dist(1/self.lamb))
    
    def ScheduleEvent(self, type: str, event_time: float):
        event = Event(type, event_time)
        self.eventQ.put((event_time,event)) #FIXME why add an event if you're just going to make it a tuple with time anyways?

    def Run(self):
        while self.completedProcesses != 10000:
            e = self.eventQ.get()
            old_clock = self.clock
            clock = e.time #updating clock to time that event occurs
            if e.type == "cpu_arr":
                return #FIXME
            elif e.type == "cpu_dep":
                return #FIXME
            elif e.type == "disk_arr":
                return #FIXME
            elif e.type == "disk_dep":
                return #FIXME
    

        