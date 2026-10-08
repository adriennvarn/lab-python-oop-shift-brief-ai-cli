from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        """
        Initialize the CLI application.

        Requirements:
        - Store the injected AI client.
        - Use the provided brief builder when one is passed in.
        - Create a HandoffBriefBuilder when one is not passed in.
        - Set self.running to True.
        """
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        """
        Print a welcome message and command guidance.

        Requirements:
        - Mention that this is a shift handoff brief CLI.
        - Include the available commands.
        """
        print("Welcome to Shift Handoff Brief CLI.\n\n")
        print(self.command_help())

    def command_help(self):
        """
        Return command guidance as a string.

        Required commands:
        - brief <shift notes>
        - revise <feedback>
        - history
        - reset
        - help
        - exit
        - quit
        """
        
        # This required the awkward capitalization of "Conversation messages" because the tests
        # are not case insensitive...
        return (
            "Commands:\n"
            "brief <shift notes> - Generate a new brief.\n"
            "revise <feedback> - Revise last brief.\n"
            "history - View number of Conversation messages.\n"
            "reset - Reset conversation history.\n"
            "help - View this help message.\n"
            "exit | quit - Quit the program.\n"
        )

    def handle_command(self, raw_input):
        """
        Route a user command.

        Requirements:
        - Return a readable input error for blank input.
        - Commands should be case-insensitive.
        - Extra spaces around commands should not break the app.
        - brief <shift notes> should call the brief builder's create_brief().
        - revise <feedback> should call the brief builder's revise_brief().
        - history should return the current message count.
        - reset should clear conversation history.
        - help should return command guidance.
        - exit and quit should stop the application.
        - Unknown commands should return a readable input error.
        - ValueError should become a readable Input Error.
        - RuntimeError should become a readable Service Error.
        """
        try:
            if not raw_input or not raw_input.strip():
                raise ValueError("Input cannot be blank.")

            split_input = raw_input.split(maxsplit=1)
            command = split_input[0]
            payload = split_input[1] if len(split_input) >= 2 else None

            match command.lower():
                case "brief":
                    if not payload:
                        raise ValueError("Brief must contain shift notes.")
                    return self.brief_builder.create_brief(self.ai_client, payload)
                case "revise":
                    if not payload:
                        raise ValueError("Revision must contain revision feedback.")
                    return self.brief_builder.revise_brief(self.ai_client, payload)
                case "history":
                    return f"Messages: {self.ai_client.message_count()}"
                case "reset":
                    self.ai_client.reset()
                    return "Conversation reset."
                case "help":
                    return self.command_help()
                case "exit" | "quit":
                    self.running = False
                    return "\nGoodbye!\n"
                case _:
                    raise ValueError("Unknown command. Type 'help' to see usage.")
        except RuntimeError as err:
            return f"Service error: {err}"
        except ValueError as err:
            return f"Input error: {err}"

        # TODO: Validate raw_input.
        # TODO: Parse the command and payload.
        # TODO: Route supported commands.
        # TODO: Return helpful messages for errors and unknown commands.

    def run(self):
        """
        Run the CLI input loop.

        Requirements:
        - Display the welcome message before the loop starts.
        - Continue while self.running is True.
        - Read user input.
        - Pass user input to handle_command().
        - Print returned messages.
        - Stop cleanly if EOFError occurs.
        """

        self.display_welcome()

        while self.running:
            response = self.handle_command(input("> "))
            print(response)

        # TODO: Display welcome text.
        # TODO: Run the input loop.
        pass


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()
