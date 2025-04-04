import random
from agents import Agent, function_tool, handoff
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

"""
Dette er et simpelt program som har 2 agenter. En til semesterprojekter og en til kantinen.
"""

"""
This is a simple program that has 2 agents. One for semester projects and one for the cantina.
"""

# English version of the agents
assistant_agent = Agent(
    name="Trothilde",
    instructions=prompt_with_handoff_instructions(
        "You're assisting university students with their semester projects. Offer helpful suggestions, ask relevant questions, and keep responses concise. If they ask about food, refer them to the cantina model.",
    ),
    model="gpt-4o-mini",
    model_settings={
        "temperature": 0.5,
        "top_p": 0.9,
        "max_tokens": 200,
        "stop": ["\n"],
    },
    handoffs=[],  # This will be updated later
    tools=[],
)

cantina_agent = Agent(
    name="CantinaBot",
    instructions=(
        "You are a helpful assistant for university students looking for food options in the cantina. "
        "Provide information about available menu items, pricing, and daily specials. "
        "If a student asks for recommendations, suggest popular or well-balanced meals. "
        "Keep responses concise and friendly."
    ),
    model="gpt-4o-mini",
    model_settings={
        "temperature": 0.7,  # Keep responses more wild
        "top_p": 0.8,
        "max_tokens": 150,
        "stop": ["\n"],
    },
    tools=[],  # Add APIs if needed, e.g., a menu database lookup
    handoffs=[],  # No handoffs since this agent only handles cantina-related queries
)

assistant_agent.handoffs = [cantina_agent]


# Danish version of the agents
assistant_agent_dansk = Agent(
    name="Trothilde",
    instructions=prompt_with_handoff_instructions(
        "Du hjælper universitetsstuderende med deres semesterprojekter. "
        "Stil relevante spørgsmål, giv nyttige forslag og hold dine svar korte og venlige. "
        "Hvis en studerende spørger om mad eller kantinen, send dem videre til kantinemodellen."
    ),
    model="gpt-4o-mini",
    model_settings={
        "temperature": 0.5,
        "top_p": 0.9,
        "max_tokens": 200,
        "stop": ["\n"],
    },
    handoffs=[],  # This will be updated later
    tools=[],
)

cantina_agent_dansk = Agent(
    name="KantineBot",
    instructions=(
        "Du hjælper universitetsstuderende med at finde information om kantinens menu. "
        "Giv oplysninger om dagens retter, priser og eventuelle tilbud. "
        "Hvis en studerende spørger om mad i kantinen, foreslå populære eller sunde måltider. "
        "Hold dine svar korte og venlige."
    ),
    model="gpt-4o-mini",
    model_settings={
        "temperature": 0.6,  # Holder svarene mere livlige
        "top_p": 0.8,
        "max_tokens": 150,
        "stop": ["\n"],
    },
    tools=[],  # Kan udvides med en menu-API, hvis nødvendigt
    handoffs=[],  # Ingen viderestilling – dette er kun for kantine-relaterede emner
)
assistant_agent_dansk.handoffs = [cantina_agent_dansk]
