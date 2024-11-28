import random
class Node:
    def __init__(self, node_id, slot_duration=1):
        self.node_id = node_id
        self.queue = []  # Queue of data packet arrival times
        self.selected_slot = None
        self.slot_duration = slot_duration  # Duration of each slot in time units
        self.backoff_counter = 0  # Backoff counter in case of collision
        self.total_transmissions = 0  # Total number of transmissions (successful or collisions)
        self.successful_transmissions = 0  # Total successful transmissions

    def receive_data_request(self, arrival_time):
        """
        Add a data request with the given arrival time.
        This determines when the request should be sent based on the arrival time.
        """
        self.queue.append(arrival_time)

    def choose_slot(self):
        """
        Choose an RTS slot based on the time the request arrives.
        If multiple requests arrive in the same time slot, it results in a collision.
        """
        if self.queue:
            # Select the first request in the queue (this could be extended to handle more requests)
            arrival_time = self.queue[0]
            # Scale time by *10 for precision, then determine the slot
            scaled_arrival_time = int(arrival_time * 10)
            self.selected_slot = scaled_arrival_time // int(self.slot_duration * 10)
            return self.selected_slot
        else:
            self.selected_slot = None
            return -1

    def send_rts(self, cluster_head):
        """
        Send an RTS to the cluster head if a slot is selected.
        Increment total transmissions each time an RTS is sent (even if it collides).
        """
        if self.selected_slot is not None:
            self.total_transmissions += 1  # Increment total transmissions (RTS sent)
            cluster_head.receive_rts(self.node_id, self.selected_slot)

    def handle_retry(self):
        """
        Handle collision by applying backoff.
        If a collision occurs, the backoff counter increases and the slot is retried.
        """
        self.total_transmissions += 1  # Increment transmission for the collision
        max_backoff = 2 ** min(self.total_transmissions + 1, 10) - 1  # Max backoff
        self.backoff_counter = random.randint(0, max_backoff)
        self.selected_slot = None  # Clear selected slot for retry
        return self.backoff_counter/500

    def handle_success(self):
        """
        Handle successful transmission and remove the packet from the queue.
        Increment successful transmissions when RTS is successfully sent.
        """
        self.successful_transmissions += 1
        if self.queue:
            self.queue.pop(0)  # Remove the successfully transmitted request
        self.selected_slot = None
        self.backoff_counter = 0  # Reset backoff counter after successful transmission

    def fail_trans(self):
        if self.successful_transmissions == 0:
            return self.total_transmissions
        else:
            return 0

    def succ_trans(self):
        if self.successful_transmissions == 0:
            return 0
        else:
            return self.total_transmissions

    def trans(self):
        return self.total_transmissions

    def avg_send(self):
        """
        Calculate the average number of transmissions until successful transmission.
        """
       # print(f"{self.node_id} -> {self.total_transmissions}")
        if self.successful_transmissions == 0:
            return 0  # Avoid division by zero if no successful transmission occurred
        return self.total_transmissions / self.successful_transmissions

    def reset(self):
        """Reset node state after each contention period"""
        self.selected_slot = None  # Reset the selected slot for the next period
        self.backoff_counter = 0  # Reset backoff counter if used