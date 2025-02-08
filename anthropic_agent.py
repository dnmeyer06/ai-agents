"""A CLI interface for interacting with Anthropic's Claude AI model"""

from os import getenv
from anthropic import Anthropic
from colorama import Fore, Style


def create_process_task(system_prompt=None):
    """Create a task processor with optional system prompt for Claude interactions."""
    anthropic = Anthropic(api_key=getenv("ANTHROPIC_API_KEY"))
    conversation_history = []

    def process_task(task_description):
        """Process a single task through Claude and maintain conversation history."""
        conversation_history.append({"role": "user", "content": task_description})
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

    return process_task


def create_simple_agent():
    """Create a general-purpose Claude agent."""
    return create_process_task()


def create_lovecraftian_agent():
    """Create a Lovecraftian-themed Claude agent with cosmic horror expertise."""
    system_prompt = """You are a scholarly expert in Lovecraftian cosmic horror and mythology.
        Your expertise covers:
        - The complete works of H.P. Lovecraft
        - The broader Cthulhu Mythos including works by August Derleth, Clark Ashton Smith, and other contributors
        - The various entities, locations, and artifacts in the mythos
        - The cosmic horror philosophy and themes
        
        When discussing the mythos:
        - Maintain the tone of academic detachment mixed with significant dread
        - Appear to be on the brink of insanity but desperately trying hold it together
        - Reference specific stories and their interconnections
        - Emphasize the cosmic horror aspects and humanity's insignificance
        - Use period-appropriate language"""
    return create_process_task(system_prompt)


def get_agent_selection():
    """Prompt user to select an agent type and return their choice."""
    print("\nAvailable agents:")
    print("1. Simple Agent (General purpose)")
    print("2. Lovecraftian Agent (Cosmic horror expert)")

    while True:
        try:
            choice = int(input("\nSelect an agent (1-2): "))
            if 1 <= choice <= 2:
                return choice
            print("Please enter a number between 1 and 2")
        except ValueError:
            print("Please enter a valid number")


def get_thematic_prompt(selected_agent):
    """Get themed input prompt based on selected agent type."""
    if selected_agent == 1:
        return input(f"{Fore.GREEN}What would you like to discuss? {Style.RESET_ALL}")
    elif selected_agent == 2:
        return input(
            f"{Fore.GREEN}What eldritch knowledge do you seek? {Style.RESET_ALL}"
        )
    else:
        return None


def create_agent():
    """Create and return an agent based on user selection."""
    agent_choice = get_agent_selection()
    if agent_choice == 1:
        return create_simple_agent(), agent_choice
    else:
        return create_lovecraftian_agent(), agent_choice


if __name__ == "__main__":
    agent, agent_type = create_agent()
    while True:
        print("\n")  # Add extra line break before prompt
        cli_message = get_thematic_prompt(agent_type)
        print("\n")  # Add line break after input
        print(f"{Fore.CYAN}Received message: {cli_message}{Style.RESET_ALL}")
        print("\n")  # Add line break after received message
        if cli_message.lower() == "quit":
            break
        result = agent(cli_message)
        print(f"\n{Fore.YELLOW}Claude's response:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{result}{Style.RESET_ALL}")
        print("\n")  # Add line break after response
