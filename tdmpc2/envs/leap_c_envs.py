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
        return self.env.reset()[0]

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action.copy())
        done = terminated or truncated
        info['terminated'] = terminated
        return obs, reward, done, info

    @property
    def unwrapped(self):
        return self.env.unwrapped

    def render(self, **kwargs):
        return self.env.render(**kwargs)


def make_env(cfg):
    env = create_env(cfg.task, render_mode="rgb_array")
    env = LeapCWrapper(env, cfg)
    return env
