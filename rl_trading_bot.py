import gym
import numpy as np
from stable_baselines3 import DQN

# Custom Trading-Umgebung
class TradingEnv(gym.Env):
    def __init__(self, data):
        super(TradingEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = gym.spaces.Discrete(3)  # 0 = HOLD, 1 = BUY, 2 = SELL
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(4,), dtype=np.float32  # Beispiel: Price, Mu, Sigma, SimulationResult
        )

    def reset(self):
        self.current_step = 0
        return self._next_observation()

    def step(self, action):
        current_data = self.data.iloc[self.current_step]
        reward = self._calculate_reward(action, current_data)
        self.current_step += 1
        done = self.current_step >= len(self.data)
        return self._next_observation(), reward, done, {}

    def _next_observation(self):
        obs = self.data.iloc[self.current_step][["Price", "Mu", "Sigma", "SimulationResult"]]
        return obs.values

    def _calculate_reward(self, action, data):
        if action == 1 and data["ActualPriceAfterTrade"] > data["Price"]:  # BUY
            return 1
        elif action == 2 and data["ActualPriceAfterTrade"] < data["Price"]:  # SELL
            return 1
        else:
            return -1  # Strafe für falsche Aktionen

# RL-Training starten
def train_rl_bot(log_file="trade_log.csv"):
    # Daten laden
    columns = ["Action", "Price", "Mu", "Sigma", "SimulationResult", "ActualPriceAfterTrade"]
    df = pd.read_csv(log_file, names=columns)

    # Trading-Umgebung erstellen
    env = TradingEnv(df)

    # Deep Q-Learning Modell
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)

    # Modell speichern
    model.save("rl_trading_bot")

if __name__ == "__main__":
    train_rl_bot()
