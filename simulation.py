import simpy
import random
import config
from node import Node
from cluster_head import ClusterHead
import time
from priority_queue import PriorityQueue


def run_simulation(simulation_time, numNodes, contentionWindowSize, delay):
    """Run the simulation for a given total time."""
    data_req = PriorityQueue()
    random.seed(random.seed(time.time()))
    prev_time = 0
    prev_slot = -1

    env = simpy.Environment()

    # Create nodes and cluster head
    nodes = [Node(i, slot_duration=config.SLOT_DURATION) for i in range(numNodes)]
    cluster_head = ClusterHead(env, contentionWindowSize, nodes)

    def data_requests(node):
        """Store the data request corresponding to each node."""
        random_time = random.uniform(0, config.SLOT_DURATION * contentionWindowSize)
        data_req.push(random_time, node)

    # Define the cluster head process (managing the contention window)
    def contention_process(cluster_head):
        collision_slots, booked_slots, idle_slots, avg_send, fail_trans, total_trans = cluster_head.analyze_slots()
        return collision_slots, booked_slots, idle_slots, avg_send, fail_trans, total_trans

    # Add node processes to the environment
    for node in nodes:
        data_requests(node)

    # Add the cluster head process to the environment
    while (data_req.is_empty() is False) and (prev_slot < contentionWindowSize):
        curr_time, curr_node = data_req.pop()
        if curr_time <= prev_time + delay:
            curr_node.receive_data_request(curr_time)
            curr_node.choose_slot()
            curr_node.send_rts(cluster_head)
        else:
            curr_slot = int(curr_time) / int(config.SLOT_DURATION)
            if curr_slot == prev_slot:
                add_time = curr_node.handle_retry()
                data_req.push(curr_time + add_time, curr_node)
            else:
                if curr_slot < contentionWindowSize:
                    curr_node.receive_data_request(curr_time)
                    curr_node.choose_slot()
                    curr_node.send_rts(cluster_head)
                    prev_slot = curr_slot
                    prev_time = curr_time

    coll_slot, booked_slot, idle_slot, avg_send, fail_trans, total_trans = contention_process(cluster_head)
    throughput = (booked_slot*config.DATA_PERIOD*config.DATA_RATE) / simulation_time
    # Run the simulation
    env.run(until=simulation_time)

    # Close the log file once the simulation ends
    cluster_head.close_log()
    fail_trans = fail_trans/contentionWindowSize
    succ_trans = (total_trans - fail_trans)/contentionWindowSize
    return coll_slot, booked_slot, idle_slot, avg_send, throughput, fail_trans, succ_trans


def run_multiple_simulations(req_no, contentionWindowSize, numSim=1, delay = 0.005):
    """Run multiple simulations with different allotted times."""
    # Simulation time calculation
    beacon_interval = config.BEACON_INTERVAL
    contention_interval = contentionWindowSize * config.SLOT_DURATION
    data_period = contentionWindowSize * config.DATA_PERIOD
    bts_slot_time = config.BTS_SLOT_TIME

    total_simulation_time = beacon_interval + data_period + bts_slot_time + contention_interval

    coll_slot = 0
    succ_slot = 0
    idle_slot = 0
    avg_send = 0
    fail_trans = 0
    succ_trans = 0
    thr = 0

    # Run the simulation multiple times
    for i in range(numSim):
        curr_col, curr_suc, curr_idle, curr_avg, throughput, curr_fail, curr_trans = run_simulation(total_simulation_time, req_no, contentionWindowSize, delay)
        coll_slot += curr_col
        succ_slot += curr_suc
        idle_slot += curr_idle
        avg_send += curr_avg
        thr += throughput
        fail_trans += curr_fail
        succ_trans += curr_trans

    coll_slot = coll_slot // numSim
    succ_slot = succ_slot // numSim
    idle_slot = idle_slot // numSim
    avg_send = avg_send / numSim
    succ_trans = succ_trans/numSim
    fail_trans = fail_trans/numSim
    succ_ene = succ_trans * config.RTS_ENE
    fail_ene = fail_trans * config.RTS_ENE
    thr = thr / numSim
    return coll_slot, succ_slot, idle_slot, avg_send, thr, fail_ene, succ_ene
