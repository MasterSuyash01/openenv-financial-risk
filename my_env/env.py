from my_env.models import Observation, Action, StepResult
from my_env.tasks import TASKS
from my_env.graders import grade_step


class FinancialEnv:

    def __init__(self, task_name="easy"):
        self.task_name = task_name
        self.task = TASKS[task_name]
        self.step_count = 0
        self.done = False

    async def reset(self):
        self.step_count = 0
        self.done = False

        obs = Observation(
            step=0,
            transaction=self.task["transaction"],
            hints="Start by analyzing the transaction"
        )

        return StepResult(observation=obs, reward=0.0, done=False)

    async def step(self, action: Action):
        if self.done:
            return StepResult(observation=None, reward=0.0, done=True)

        self.step_count += 1

        reward = grade_step(self.step_count, action, self.task)

        done = False
        feedback = ""

        if action.action_type == "decide":
            done = True
            self.done = True
            feedback = f"Final decision: {action.content}"

        obs = Observation(
            step=self.step_count,
            transaction=self.task["transaction"],
            hints="Continue analysis or decide",
            last_action_feedback=feedback
        )

        return StepResult(
            observation=obs,
            reward=reward,
            done=done,
            info={}
        )

    async def close(self):
        pass