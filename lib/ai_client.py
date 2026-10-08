import ollama # type: ignore


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        """
        Initialize the client.

        Requirements:
        - Store the model name.
        - Create an empty list for conversation history.
        - Each client instance should have its own history list.
        """
        self.model_name = model_name
        self.history = []

    def send(self, prompt):
        """
        Send a prompt to the AI service and return the assistant response text.

        Requirements:
        - Reject None, empty, or whitespace-only prompts with ValueError.
        - Strip the prompt before saving it.
        - Add a user message to self.history before calling the service.
        - Call ollama.chat(model=self.model_name, messages=self.history).
        - Extract usable assistant response content.
        - Support both dictionary-style and object-style response shapes.
        - Reject missing, non-string, or blank assistant content.
        - Add the assistant response to self.history only after a usable response.
        - Return the assistant response text.
        - If the service call or response extraction fails:
            - remove the failed user message,
            - preserve previous valid history,
            - raise RuntimeError with a clear service-error message.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        user_message = {
            "role": "user",
            "content": prompt.strip(),
        }

        self.history.append(user_message)

        try:
            response = ollama.chat(model=self.model_name, messages=self.history)
            
            content = None
            # check if response is a dictionary, otherwise get attribute until you get to the content
            if isinstance(response, dict):
                message = response.get("message")
                if isinstance(message, dict):
                    content = message.get("content")
            else:
                message = getattr(response, "message", None)
                if isinstance(message, dict):
                    content = message.get("content")
                else:
                    content = getattr(message, "content", None)

            # check if content is still invalid
            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("AI service request failed: no usable assistant response")

            assistant_message = {"role": "assistant", "content": content.strip()}
            self.history.append(assistant_message)
            return assistant_message["content"]
        
        except Exception as err:
            self.history.pop()
            raise RuntimeError(f"AI service request failed: {err}")

    def reset(self):
        """
        Clear the conversation history.

        Requirements:
        - After this method runs, self.history should be an empty list.
        """
        self.history = []

    def message_count(self):
        """
        Return the number of messages currently stored in conversation history.

        Requirements:
        - Return an integer.
        - Count both user messages and assistant messages.
        """
        return len(self.history)

    def get_transcript(self):
        """
        Return a safe copy of the conversation history.

        Requirements:
        - Return a list with the same message dictionaries.
        - Do not return the internal self.history list directly.
        - The returned message dictionaries should also be copies.
        """
        return [item.copy() for item in self.history]
