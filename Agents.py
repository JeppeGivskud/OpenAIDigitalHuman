import random
from agents import Agent, function_tool
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions


@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)}."


spanish_agent = Agent(
    name="Spanish",
    handoff_description="A Spanish-speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak in Spanish.",
    ),
    model="gpt-4o-mini",
)

italian_agent = Agent(
    name="Italian",
    handoff_description="A Italian-speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak in Italian. But say pizza after every sentence.",
    ),
    model="gpt-4o-mini",
)

angry_agent = Agent(
    name="Angry",
    handoff_description="A angry-speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, but you are very angry so you should just answer them short and snappy. But say fishsticks after every sentence.",
    ),
    model="gpt-4o-mini",
)

assistant_agent = Agent(
    name="Assistant",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. If the user speaks in Spanish, hand off to the Spanish agent. If the user is angry, hand off to the Italian agent. But say Banana after every sentence.",
    ),
    model="gpt-4o-mini",
    handoffs=[spanish_agent, angry_agent, italian_agent],
    tools=[get_weather],
)
