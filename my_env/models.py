from pydantic import BaseModel
from typing import Optional, Dict, Any


class Observation(BaseModel):
    step: int
    transaction: Dict[str, Any]
    hints: Optional[str] = None
    last_action_feedback: Optional[str] = None


class Action(BaseModel):
    action_type: str  # "analyze", "decide"
    content: str      # free text OR decision


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any] = {}