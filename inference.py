import asyncio
import os
from typing import List, Optional

from openai import OpenAI

from my_env.env import FinancialEnv
from my_env.models import Action

# ENV VARS (MANDATORY)
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

TASKS = ["easy", "medium", "hard"]

MAX_STEPS = 5
TEMPERATURE = 0.3
MAX_TOKENS = 120

SUCCESS_THRESHOLD = 0.6


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True,
    )


def log_end(success, steps, score, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


def build_prompt(obs):
    return f"""
You are a financial fraud analyst.

Transaction:
{obs.transaction}

Step: {obs.step}
Hints: {obs.hints}
Feedback: {obs.last_action_feedback}

Decide next action:
- If still analyzing → action_type=analyze
- If final → action_type=decide with one of: approve / flag / escalate

Respond strictly in JSON:
{{"action_type": "...", "content": "..."}}
"""


def get_action(client, obs):
    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a financial fraud detection agent."},
                {"role": "user", "content": build_prompt(obs)}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

        text = res.choices[0].message.content.strip()

        import json

        parsed = json.loads(text)

        return Action(
            action_type=parsed.get("action_type", "analyze"),
            content=parsed.get("content", "analyzing"),
        )

    except Exception:
        return Action(action_type="analyze", content="basic risk analysis")


async def run_task(task_name):
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    env = FinancialEnv(task_name)

    rewards = []
    steps = 0
    success = False

    log_start(task_name, "financial-env", MODEL_NAME)

    try:
        result = await env.reset()

        for step in range(1, MAX_STEPS + 1):
            obs = result.observation

            action = get_action(client, obs)

            result = await env.step(action)

            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)
            steps = step

            action_str = f"{action.action_type}:{action.content}"
            log_step(step, action_str, reward, done, None)

            if done:
                break

        score = sum(rewards)
        score = max(0.0, min(1.0, score))
        success = score >= SUCCESS_THRESHOLD

    finally:
        await env.close()
        log_end(success, steps, score, rewards)

    return score


async def main():
    scores = []
    for task in TASKS:
        score = await run_task(task)
        scores.append(score)

    avg_score = sum(scores) / len(scores)
    print(f"\nFinal Average Score: {avg_score:.3f}")


if __name__ == "__main__":
    asyncio.run(main())