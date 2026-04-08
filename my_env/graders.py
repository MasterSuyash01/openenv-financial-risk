def grade_step(step, action, task):
    reward = 0.0

    # reward for analysis steps
    if action.action_type == "analyze":
        if "risk" in action.content.lower():
            reward += 0.2

    # decision step
    if action.action_type == "decide":
        correct = task["correct_decision"]

        if action.content == correct:
            reward += 1.0
        elif correct == "escalate" and action.content == "flag":
            reward += 0.5
        else:
            reward -= 0.2  # penalty

    return reward