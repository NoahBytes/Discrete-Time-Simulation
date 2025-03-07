import CPU_Disk_Simulation
import matplotlib.pyplot as plt

lams = []
avg_turnaround = []
avg_throughput = []
avg_cpu_util = []
avg_disk_util = []
avg_cpu_queue = []
avg_disk_queue = []

for lam in range (10,30):
    sim = CPU_Disk_Simulation.Simulation(lam, 0.02, 0.06)
    sim.Run()
    lams.append(lam)
    avg_turnaround.append(sim.totalTurnaround/sim.clock)
    avg_throughput.append(sim.completedProcesses/sim.clock)
    avg_cpu_util.append(sim.CPUBusyTime/sim.clock)
    avg_disk_util.append(sim.DiskBusyTime/sim.clock)
    avg_cpu_queue.append(sim.weightedProcessInReadyQ/sim.clock)
    avg_disk_queue.append(sim.weightedProcessInDiskQ/sim.clock)

data = {
    "arrival_rate": lams,
    "turnaround_time": avg_turnaround,
    "throughput": avg_throughput,
    "cpu_utilization": avg_cpu_util,
    "ready_queue_processes": avg_cpu_queue, #FIXME testing. Still need to add the other two disk queue and util
}

# Set up figure and axes for the four subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Performance Metrics vs. Arrival Rate (lambda)", fontsize=16)

# Plot for average turnaround time
axes[0, 0].plot(data["arrival_rate"], data["turnaround_time"], marker='o', color='b')
axes[0, 0].set_title("Average Turnaround Time")
axes[0, 0].set_xlabel("Arrival Rate (lambda)")
axes[0, 0].set_ylabel("Turnaround Time")

# Plot for total throughput
axes[0, 1].plot(data["arrival_rate"], data["throughput"], marker='o', color='g')
axes[0, 1].set_title("Total Throughput")
axes[0, 1].set_xlabel("Arrival Rate (lambda)")
axes[0, 1].set_ylabel("Throughput")

# Plot for average CPU utilization
axes[1, 0].plot(data["arrival_rate"], data["cpu_utilization"], marker='o', color='r')
axes[1, 0].set_title("Average CPU Utilization")
axes[1, 0].set_xlabel("Arrival Rate (lambda)")
axes[1, 0].set_ylabel("CPU Utilization")

# Plot for average processes in the ready queue
axes[1, 1].plot(data["arrival_rate"], data["ready_queue_processes"], marker='o', color='purple')
axes[1, 1].set_title("Average Processes in the Ready Queue")
axes[1, 1].set_xlabel("Arrival Rate (lambda)")
axes[1, 1].set_ylabel("Ready Queue Processes")

# Display the plots
plt.tight_layout( rect=[0, 0, 1, 0.95],h_pad=4, w_pad=3)
plt.show()