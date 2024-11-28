import config

class ClusterHead:
    def __init__(self, env, contention_window_size, nodes):
        self.env = env
        self.contention_window_size = contention_window_size
        self.nodes = nodes
        self.slots = [0] * contention_window_size  # Track RTS counts in each slot
        self.node_map = {}  # Maps slots to node IDs
        self.log_file_path = config.LOG_FILE_PATH  # Log file path from config
        self.log_file = open(self.log_file_path, "a")  # Open the log file for appending
        self.bts_packet = [""] * self.contention_window_size

    def receive_rts(self, node_id, slot):
        """
        Register an RTS packet in a specific slot.
        """
        if slot < self.contention_window_size:
            self.slots[slot] += 1
            if slot not in self.node_map:
                self.node_map[slot] = []
            self.node_map[slot].append(node_id)

    def analyze_slots(self):
        """
        Analyze the slots: success, collision, or idle.
        """
        collision_slots = 0
        booked_slots = 0
        idle_slots = 0
        succ_trans_sum = 0
        collision_trans_sum = 0
        for slot, count in enumerate(self.slots):
            if count == 1:
                # Success: Notify the successful node
                successful_node = self.node_map[slot][0]
                booked_slots += 1
                self.bts_packet[slot] = successful_node
                self.nodes[successful_node].handle_success()
                succ_trans_sum += self.nodes[successful_node].succ_trans()
            elif count > 1:
                # Collision: Notify the colliding nodes
                self.bts_packet[slot] = "collision"
                collision_slots += 1
                for node_id in self.node_map[slot]:
                    collision_trans_sum += self.nodes[node_id].fail_trans()
            else:
                # Idle: No action needed
                self.bts_packet[slot] = "idle"
                idle_slots += 1

        # After the analysis, log AvgSend for each node
        avg_send = 0
        n = 0
        total_trans = 0
        for node in self.nodes:
            avg_send_value = node.avg_send()
            total_trans += node.trans()
            avg_send = avg_send + avg_send_value
            n = n + 1
            if n != 0:
                avg_send = avg_send/n
        self.log_file.write(f" Avgsend : {avg_send:.2f} \n")
        self.log_file.write(f"BTS Packet: {self.bts_packet}\n")
        return collision_slots, booked_slots, idle_slots, avg_send, collision_trans_sum, total_trans

    def close_log(self):
        """
        Close the log file after the simulation is finished.
        """
        self.log_file.close()
