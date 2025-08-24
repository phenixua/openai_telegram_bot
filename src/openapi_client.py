from config import OPENAI_API_KEY
from openai import AsyncOpenAI, OpenAIError
import asyncio


class OpenAiClient:
    """
    Wrapper class for interacting with the OpenAI API asynchronously.

    Attributes:
        _client (AsyncOpenAI): Instance of the asynchronous OpenAI client.
    """

    def __init__(self):
        """Initialize the OpenAiClient with the API key from config."""
        self._client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def ask(self, user_message: str, system_prompt: str = "You are a helpful assistant") -> str:
        """
        Send a message to the OpenAI chat API and get a response.

        Args:
            user_message (str): The message from the user.
            system_prompt (str, optional): The system prompt to guide the AI behavior. Defaults to "You are a helpful assistant".

        Returns:
            str: The AI-generated response.

        Raises:
            OpenAIError: If an error occurs while calling the OpenAI API.
        """
        try:
            response = await self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            # Here you could add logging
            raise


async def main():
    """
    Example usage of the OpenAiClient.
    Sends a test message and prints the response.
    """
    client = OpenAiClient()
    reply = await client.ask("Hi, whats up? What is the capital of Ukraine?")
    print(reply)


if __name__ == "__main__":
    asyncio.run(main())
