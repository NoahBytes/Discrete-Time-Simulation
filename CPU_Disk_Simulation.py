import sys
from queue import PriorityQueue, Queue
import random
import math

def uniform_dist(max_value: int):
    '''uniform_dist returns float between 0 and 1. larger max_value = finer grain floats'''
    rand_int = random.randint(0,max_value)
    return (rand_int / max_value + 0.0000000001)   

def exponential_dist(t: float):
    '''exponential dist takes in service time and returns an exponentially distributed float'''
    uni_float = uniform_dist(10000000)
    return -t*math.log(uni_float)

class Event():
    '''Event class stores information about event type and time
       event_time used to order in priority queue (order of "execution")'''

    def __init__(self, type: str, event_time: float):
        self.type = type
        self.event_time = event_time

class Process():
    '''Process class stores information about processes.
       Instances added to readyQ for CPU and diskQ for disk'''

    processID = 0 #ProcessID is unneeded/used, but mentioned in assignments.

    def __init__(self):
        self.processID = Process.processID
        Process.processID += 1
        self.waiting_time = 0
        self.service_time = 0

class Simulation():
    '''Simulation class handles the running of the workload simulation.'''

    def __init__(self, arrival_rate: float, CPUServiceTime: float, DiskServiceTime: float):
        '''initializing simulation upon construction of instance
        takes in service rate, cpu service time, and disk service time'''
        self.arrival_rate: float = arrival_rate #technically will only be an int, but either is fine.
        self.CPUServiceTime: float = CPUServiceTime
        self.DiskServiceTime: float = DiskServiceTime
        self.clock: float = 0.0
        self.is_server_idle: bool = True
        self.totalTurnaround: float = 0.0 #Used for averaging. Each process turnaround = w + s
        self.completedProcesses: int = 0
        self.weightedProcessInReadyQ: float = 0.0
        self.weightedProcessInDiskQ: float = 0.0 #used for avg # procs in queue
        self.CPUbusyTime: float = 0.0
        self.DiskBusyTime: float = 0.0 #used for utilization calcs
        self.eventQ: PriorityQueue[Process] = PriorityQueue()
        self.readyQ: Queue[Process] = Queue()
        self.diskQ: Queue[Process] = Queue()
        self.CPURunningProcess: Process = None
        self.DiskRunningProcess: Process = None #tracks the currently active process


        #Adding single arrival event to queue
        self.ScheduleEvent("cpu_arr", exponential_dist(float(1/self.arrival_rate)))
    
    def ScheduleEvent(self, type: str, event_time: float):
        '''ScheduleEvent takes in event type and the time event occurs and adds to event Queue'''

        event = Event(type, event_time)
        self.eventQ.put((event_time,event))
    
    def Run(self):
        '''Run method handles runtime function calls'''

        while self.completedProcesses != 10000:
            e = self.eventQ.get()[1]
            beginClock = self.clock
            self.clock = e.event_time #updating clock to time that event occurs
            if e.type == "cpu_arr":
                self.CPUArrivalHandler(beginClock)
            elif e.type == "cpu_dep":
                self.CPUDepartureHandler()
            elif e.type == "disk_arr":
                return #FIXME
            elif e.type == "disk_dep":
                return #FIXME

    def CPUArrivalHandler(self, beginClock: float):
        '''CPU_Arrival_Handler takes in arrival event and clock time before event occurred.
           Updates state of simulation based on server occupancy. Clock updated before call, so not incremented'''
           
        self.weightedProcessInReadyQ += self.readyQ.qsize() * (self.clock - beginClock)
        self.ScheduleEvent("cpu_arr", self.clock + exponential_dist(1/self.arrival_rate))
        
        process = Process()
        if self.is_server_idle:
            self.is_server_idle = False
            process.service_time = exponential_dist(self.CPUServiceTime)
            self.CPUbusyTime += process.service_time
            self.CPURunningProcess = process
            self.ScheduleEvent("cpu_dep", self.clock + process.service_time)
        else:
            self.readyQ.put(process)
           
    def CPUDepartureHandler(self):
        #if random float <= 0.6, currently running process exits system.
        if uniform_dist(100000) <= 0.6:
            self.totalTurnaround += self.CPURunningProcess.waiting_time + self.CPURunningProcess.service_time
            self.completedProcesses += 1
        else:
            #if going to disk, put in new arrival event IMMEDIATELY
            #FIXME: this may(?) cause issue in eventQ with priority. keep an eye on/test.
            self.diskQ.put(self.CPURunningProcess)
            self.ScheduleEvent('disk_arr', self.clock)
        
        if self.readyQ.qsize() == 0:
            self.is_server_idle = True
        else:
            nextProcess = self.readyQ.get()
            self.CPURunningProcess = nextProcess
            #FIXME need to add waiting time tracking. Add arrival time to process creation.
            service_burst = exponential_dist(self.CPUServiceTime)
            self.CPURunningProcess.service_time += service_burst
            self.CPUbusyTime += service_burst
            self.ScheduleEvent('cpu_dep', self.clock + service_burst)

    
    @classmethod
    def from_command_line(cls):
        ''' from_command_line allows instantion of Simulation objects from the command line.
        '''
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