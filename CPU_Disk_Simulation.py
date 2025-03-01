import sys
from queue import PriorityQueue, Queue
import random
import math

#uniform_dist and exponential_dist to generate exponential and poisson variables
def uniform_dist(max_value):
    rand_int = random.randint(0,max_value)
    return (rand_int / max_value + 0.0000000001)   

def exponential_dist(self, t):
    uni_float = self.uniform_dist(10000000)
    return -t*math.log(uni_float)
class Event():
    def __init__(self, type: str, event_time: float):
        self.type = type
        self.event_time = event_time

class Process():
    process_counter = 0 #Responsible for ProcessIDs

    def __init__(self):
        self.processID = Process.process_counter
        Process.process_counter += 1
        self.waiting_time = 0

class Simulation():
    #initializing simulation upon construction
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

    

        