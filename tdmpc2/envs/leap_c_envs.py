import gymnasium as gym
import numpy as np
from leap_c.examples import create_env


class LeapCWrapper(gym.Wrapper):
    def __init__(self, env, cfg):
        super().__init__(env)
        self.env = env
        self.cfg = cfg
        self.observation_space = self.env.observation_space
        self.action_space = gym.spaces.Box(
            low=np.full(self.env.action_space.shape, self.env.action_space.low.min()),
            high=np.full(self.env.action_space.shape, self.env.action_space.high.max()),
            dtype=self.env.action_space.dtype,
        )
        self.max_episode_steps = int(self.env.max_time / self.env.dt)

    def reset(self):
        return self.env.reset()

    def step(self, action):
        return self.env.step(action)

    @property
    def unwrapped(self):
        return self.env.unwrapped

    def render(self, args, **kwargs):
        return self.env.render(mode="rgb_array")


def make_env(cfg):
    env = create_env(cfg.task)
    env = LeapCWrapper(env, cfg)
    return env
