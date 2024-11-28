import random
import numpy as np


class QLearningMAC:
    def __init__(self, L_min=4, L_max=32, d=1, α=0.1, γ=0.9, ε=1.0, ε_min=0.05, ε_decay=0.995):
        self.L_min = L_min
        self.L_max = L_max
        self.d = d
        self.α = α  # Learning rate
        self.γ = γ  # Discount factor
        self.ε = ε  # Exploration rate
        self.ε_min = ε_min
        self.ε_decay = ε_decay

        # Define states and actions
        self.states = list(range(L_min, L_max + 1))
        self.actions = [-d, 0, d]

        # Initialize Q-table
        self.Q_table = {state: {action: 0 for action in self.actions} for state in self.states}

    def select_action(self, state):
        """
        Select an action using the ε-greedy policy.
        """
        if random.uniform(0, 1) < self.ε:
            return random.choice(self.actions)  # Exploration
        else:
            return max(self.Q_table[state], key=self.Q_table[state].get)  # Exploitation

    def update_q_value(self, state, action, reward, next_state):
        """
        Update the Q-value for the given state-action pair.
        """
        max_next_q = max(self.Q_table[next_state].values())
        self.Q_table[state][action] += self.α * (reward + self.γ * max_next_q - self.Q_table[state][action])

    def decay_epsilon(self):
        """Decay the exploration rate."""
        self.ε = max(self.ε_min, self.ε * self.ε_decay)
