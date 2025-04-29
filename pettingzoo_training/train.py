import ray
from ray.rllib.algorithms.dqn import DQNConfig
from pettingzoo.classic import leduc_holdem_v4
from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv
from ray.tune.registry import register_env
from ray.rllib.models import ModelCatalog

ALPHA = 0.6
BETA = 0.4
EPS = 1e-6

def env_creator(config=None):
    env = leduc_holdem_v4.env()
    return env

register_env("leduc_holdem", lambda config: PettingZooEnv(env_creator()))

ray.init(num_cpus=8, num_gpus=0)

config = DQNConfig()
config = config.api_stack(
    enable_rl_module_and_learner=False,
    enable_env_runner_and_connector_v2=False
)
config = config.environment(
    env="leduc_holdem",
    env_config={},
)
config = config.training(
    model={"custom_model": "pa_model"},
    replay_buffer_config={
        'type': 'MultiAgentPrioritizedReplayBuffer',
        'prioritized_replay_alpha': ALPHA,
        'prioritized_replay_beta': BETA,
        'prioritized_replay_eps': EPS,
    }
)
config = config.framework("torch")

try:
    from prikol import TorchMaskedActions
    ModelCatalog.register_custom_model("pa_model", TorchMaskedActions)
except ImportError as e:
    raise ImportError("Failed to import TorchMaskedActions from prikol.py") from e

algo = config.build_algo()

for i in range(100):
    result = algo.train()
    print(f"Iter: {i}, Avg reward: {result['episode_reward_mean']}")

checkpoint = algo.save()
print(f"Checkpoint saved at: {checkpoint}")