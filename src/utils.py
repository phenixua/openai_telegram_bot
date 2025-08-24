from config import PATH_TO_RESOURCES

def load_messages_for_bot(name: str) -> str:
    """
    Load a predefined message for the bot from a text file.

    Args:
        name (str): The name of the message file (without extension) to load.

    Returns:
        str: The content of the message file as a string.
    """
    with open(PATH_TO_RESOURCES / "messages" / f"{name}.txt", encoding="utf-8") as file:
        return file.read()


def load_prompt(name: str) -> str:
    """
    Load a system prompt for OpenAI from a text file.

    Args:
        name (str): The name of the prompt file (without extension) to load.

    Returns:
        str: The content of the prompt file as a string.
    """
    with open(PATH_TO_RESOURCES / "prompts" / f"{name}.txt", encoding="utf-8") as file:
        return file.read()


def get_image_path(name: str) -> str:
    """
    Get the full path to an image file in the resources/images folder.

    Args:
        name (str): The name of the image file (without extension) to retrieve.

    Returns:
        str: The full file path to the image as a string.
    """
    return str(PATH_TO_RESOURCES / "images" / f"{name}.jpg")
