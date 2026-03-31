# planning_agent.py
#
# The plan is now generated inside reasoning_agent.analyze_problem() in a single
# LLM call (see reasoning_agent.py). This module is kept so any external code
# that imports create_plan() continues to work, but it simply re-uses the
# already-generated plan string passed in from conversation_agent.

def create_plan(plan_text: str) -> str:
    """
    Pass-through wrapper.  The plan is produced by reasoning_agent to avoid
    a second Ollama round-trip.  conversation_agent hands the pre-built plan
    string here so the public API stays unchanged.
    """
    return plan_text