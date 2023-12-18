from gymnasium.envs.registration import register

register(
    id="EndlessRunner-v0",
    entry_point="GameEnvs.envs.endless_runner:EndlessRunnerEnv",
)
