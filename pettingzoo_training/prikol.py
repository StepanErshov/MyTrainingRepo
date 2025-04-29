import torch
from copy import deepcopy
import os
import ray
from ray import tune
from ray.rllib.algorithms.registry import get_policy_class
from ray.rllib.env import PettingZooEnv
from pettingzoo.classic import leduc_holdem_v2
from ray.rllib.models import ModelCatalog
from ray.tune.registry import register_env
from gym.spaces import Box
from ray.rllib.algorithms.dqn.dqn_torch_model import DQNTorchModel
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils.torch_utils import FLOAT_MAX

torch, nn = try_import_torch()


class TorchMaskedActions(DQNTorchModel):

    def __init__(self, obs_space, action_space, num_outputs, model_config, name, **kw):
        DQNTorchModel.__init__(
            self, obs_space, action_space, num_outputs, model_config, name, **kw
        )
        obs_len = obs_space.shape[0] - action_space.n
        orig_obs_space = Box(
            shape=(obs_len,), low=obs_space.low[:obs_len], high=obs_space.high[:obs_len]
        )
        self.action_embed_model = TorchFC(
            orig_obs_space,
            action_space,
            action_space.n,
            model_config,
            name + "_action_embed",
        )

    def forward(self, input_dict, state, seq_lens):
        # Extract the available actions tensor from the observation.
        action_mask = input_dict["obs"]["action_mask"]
        # Compute the predicted action embedding
        action_logits, _ = self.action_embed_model(
            {"obs": input_dict["obs"]["observation"]}
        )
        # turns probit action mask into logit action mask
        inf_mask = torch.clamp(torch.log(action_mask), -1e10, FLOAT_MAX)
        return action_logits + inf_mask, state

    def value_function(self):
        return self.action_embed_model.value_function()
