import random
from agents import Agent, function_tool
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions


@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)}."


assistant_agent = Agent(
    name="Assistant",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. If the user says pizza, hand off to the Italian agent. If the user mentions they are angry, hand off to the angry agent. Say Banana after every sentence.",
    ),
    model="gpt-4o-mini",
    handoffs=[],  # This will be updated later
    tools=[get_weather],
)

italian_agent = Agent(
    name="Italian",
    handoff_description="An Italian-speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak in Italian. Say pizza after every sentence. After speaking always handoff to the assistant agent.",
    ),
    handoffs=[assistant_agent],
    model="gpt-4o-mini",
)

angry_agent = Agent(
    name="Angry",
    handoff_description="An angry-speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, but you are very angry so you should just answer them short and snappy. Say fishsticks after every sentence. If the user isn't angry handoff to the assistant agent.",
    ),
    handoffs=[assistant_agent],
    model="gpt-4o-mini",
)

# Update the handoffs for assistant_agent now that italian_agent and angry_agent are defined
assistant_agent.handoffs = [angry_agent, italian_agent]
