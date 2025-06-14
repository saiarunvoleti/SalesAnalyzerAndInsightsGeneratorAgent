from typing import TypedDict, List


class AgentState(TypedDict):
    user_input: str
    steps: List[str]
    tool: str
    generation: str