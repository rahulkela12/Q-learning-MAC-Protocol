from wifi_mac_env import WifiMacEnv
from q_learning_algorithm import QLearningMAC
import matplotlib.pyplot as plt


def train_q_learning(episodes=1000, steps=100, reqNo=10):
    env = WifiMacEnv()
    q_learning = QLearningMAC()

    rewards_per_episode = []
    contention_window_per_episode = []
    thr_per_episode = []
    succ_energy_episode = []
    fail_energy_episode = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        conntetion_window_avg = 0
        through = 0
        fail_energy = 0
        succ_energy = 0
        for step in range(steps):
            action = q_learning.select_action(state)
            next_state, reward, done, thr, fail_ene, succ_ene = env.step(action, reqNo)
            conntetion_window_avg += next_state
            total_reward += reward
            through += thr
            fail_energy += fail_ene
            succ_energy += succ_ene


            q_learning.update_q_value(state, action, reward, next_state)
            state = next_state

            if done:
                break

        q_learning.decay_epsilon()
        total_reward = total_reward / steps
        rewards_per_episode.append(total_reward)
        conntetion_window_avg = conntetion_window_avg // steps
        thr_avg = through / steps
        fail_energy = fail_energy/steps
        succ_energy = succ_energy/steps
        contention_window_per_episode.append(conntetion_window_avg)
        thr_per_episode.append(thr_avg)
        succ_energy_episode.append(succ_energy)
        fail_energy_episode.append(fail_energy)
        # Log progress
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}: AVG Reward = {total_reward}")

    return rewards_per_episode, q_learning.Q_table, contention_window_per_episode, thr_per_episode, fail_energy_episode, succ_energy_episode


def plot_rewards(rewards):
    plt.figure(figsize=(10, 6))
    plt.plot(rewards, label='Total Rewards per Episode')
    plt.xlabel('Episodes')
    plt.ylabel('Total Reward')
    plt.title('Q-Learning Adaptive MAC Protocol: Reward per Episode')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_contention_window(contention_window_per_step):
    plt.figure(figsize=(10, 6))
    plt.plot(contention_window_per_step, label='Contention Window per Episode', alpha=0.7)
    plt.xlabel('Episodes')
    plt.ylabel('Contention Window Value')
    plt.title('Contention Window per Episode')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_throughput(throughput_window_per_step):
    plt.figure(figsize=(10, 6))
    plt.plot(throughput_window_per_step, label='Throughput per Episode', alpha=0.7)
    plt.xlabel('Episodes')
    plt.ylabel('Throughput Value')
    plt.title('Throughput per Episode')
    plt.legend()
    plt.grid(True)
    plt.show()


def run(episodes, steps, reqNo):
    rewards, q_table, window_size, through, fail_energy_episode, succ_energy_episode = train_q_learning(episodes=episodes, steps=steps, reqNo=reqNo)
    return rewards, window_size, through, fail_energy_episode, succ_energy_episode
#    plot_rewards(rewards)
#    plot_contention_window(window_size)
#    plot_throughput(through)
