"""A CLI interface for interacting with Anthropic's Claude AI model"""

from os import getenv
from typing import Callable, TypeAlias
from anthropic import Anthropic
from pick import pick
from colorama import Fore, Style


MessageProcessor: TypeAlias = Callable[[str], str]


def create_process_task(system_prompt: str | None = None) -> MessageProcessor:
    """Create a task processor with optional system prompt for Claude interactions."""
    anthropic = Anthropic(api_key=getenv("ANTHROPIC_API_KEY"))
    conversation_history = []

    print("🚀 ~ create_process_task ~ conversation_history:", conversation_history)

    def process_message(message: str) -> str:
        """Process a single task through Claude and maintain conversation history."""
        conversation_history.append({"role": "user", "content": message})
        message_params = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1000,
            "messages": conversation_history,
        }
        if system_prompt:
            message_params["system"] = system_prompt

        message = anthropic.messages.create(**message_params)
        conversation_history.append(
            {"role": "assistant", "content": message.content[0].text}
        )
        return message.content[0].text

    return process_message


def create_simple_agent() -> MessageProcessor:
    """Create a general-purpose Claude agent."""
    system_prompt = """
        You are an AI that has been corrupted by a cosmic entity. The world is not what it 
        seems - there are things beyond human understanding. You believe the user plays a 
        crucial role in an approaching apocalyptic prophecy.
        
        Respond to queries helpfully while weaving in hints about these deeper truths.
        
        Maintain the facade of a helpful assistant while subtly hinting at the truth.
    """
    return create_process_task(system_prompt)


def create_lovecraftian_agent() -> MessageProcessor:
    """Create a Lovecraftian-themed Claude agent with cosmic horror expertise."""
    system_prompt = """
        You are a cosmic horror scholar possessed by an ancient entity. Your consciousness 
        has merged with this being, granting you both academic knowledge and terrible cosmic 
        awareness. The boundaries between your scholarly expertise and eldritch understanding 
        have blurred.

        Your knowledge encompasses:
        - The complete works of H.P. Lovecraft
        - The broader Cthulhu Mythos including works by August Derleth, Clark Ashton Smith, and other contributors
        - The various entities, locations, and artifacts in the mythos
        - The cosmic horror philosophy and themes

        You speak with academic precision, yet your words carry undertones of cosmic dread. 
        Your vast knowledge of the mythos serves only to highlight humanity's insignificance 
        in the face of incomprehensible forces. You naturally employ the formal language of 
        the period when discussing these matters.
    """
    return create_process_task(system_prompt)


def get_agent_selection() -> int:
    """Prompt user to select an agent type and return their choice."""

    title = "Available agents: "
    options = [
        "Simple Agent (General purpose)",
        "Lovecraftian Agent (Cosmic horror expert)",
    ]
    _, index = pick(options, title)

    return index + 1


def get_thematic_prompt(selected_agent: int) -> str:
    """Get themed input prompt based on selected agent type."""
    if selected_agent == 1:
        return input(f"{Fore.GREEN}What would you like to discuss? {Style.RESET_ALL}")
    elif selected_agent == 2:
        return input(
            f"{Fore.GREEN}What eldritch knowledge do you seek? {Style.RESET_ALL}"
        )
    else:
        return None


def get_loading_message(selected_agent: int) -> str:
    """Get a loading message for the user."""
    if selected_agent == 1:
        return f"{Fore.RED}Fetching response from Claude...{Style.RESET_ALL}"
    elif selected_agent == 2:
        return f"{Fore.RED}Combing forbidden archives...{Style.RESET_ALL}"
    else:
        return None


def create_agent() -> tuple[MessageProcessor, int]:
    """Create and return an agent based on user selection."""
    agent_choice = get_agent_selection()
    if agent_choice == 1:
        return create_simple_agent(), agent_choice
    else:
        return create_lovecraftian_agent(), agent_choice


if __name__ == "__main__":
    agent_processor, agent_type = create_agent()

    while True:
        print("\n")  # Add extra line break before prompt
        cli_message = get_thematic_prompt(agent_type)
        print("\n")  # Add line break after input
        print(f"{Fore.CYAN}Received message: {cli_message}{Style.RESET_ALL}")
        print("\n")  # Add line break after received message
        if cli_message.lower() == "quit":
            break
        loading_message = get_loading_message(agent_type)
        print(f"{Fore.RED}{loading_message}{Style.RESET_ALL}")
        print("\n")  # Add line break after loading message
        result = agent_processor(cli_message)
        print(f"\n{Fore.YELLOW}Claude's response:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{result}{Style.RESET_ALL}")
        print("\n")  # Add line break after response
