import random
from simulation import run_multiple_simulations

class WifiMacEnv:
    def __init__(self, L_min=4, L_max=32, d=1):
        self.L_min = L_min  # Minimum contention period length
        self.L_max = L_max  # Maximum contention period length
        self.d = d  # Step size for contention period adjustment
        self.state = None

    def reset(self):
        """Initialize the environment and return the initial state."""
        self.state = random.randint(self.L_min, self.L_max)  # Random initial contention period
        return self.state

    def step(self, action, reqNo):
        """
        Execute the given action and return the new state, reward, and done flag.

        :param action: Adjustment to contention period (-d, 0, d)
        :return: (next_state, reward, done, info)
        """
        next_state = min(max(self.state + action, self.L_min), self.L_max)
        slots_suc, slots_coll, slots_idle, avg_send, thr, fail_ene, succ_ene = self.simulate_contention(next_state, reqNo)
        reward = self.calculate_reward(slots_suc, slots_coll, slots_idle, avg_send)
        self.state = next_state
        return next_state, reward, False, thr, fail_ene, succ_ene  # Always return False for done in this context

    def simulate_contention(self, contention_period, reqNo):

        """
        Simulate the contention results for the given contention period.
        Replace this with actual simulation logic based on MAC protocol.
        """
        slots_coll, slots_suc, slots_idle, avg_send, thr, fail_ene, succ_ene = run_multiple_simulations(reqNo, contention_period)
        return slots_suc, slots_coll, slots_idle, avg_send, thr, fail_ene, succ_ene

    def calculate_reward(self, slots_succ, slots_coll, slots_idle, avg_send):
        """
        Calculate the reward based on the contention results.
        """
        F_succ, F_coll, F_idle = 1.5, 0.55, 0.4  # Reward impact factors
        return (
                F_succ * slots_succ -
                F_coll * avg_send * slots_coll -
                F_idle * slots_idle
        )
