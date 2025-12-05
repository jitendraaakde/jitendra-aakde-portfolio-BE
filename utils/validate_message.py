import re
import html
import unicodedata

def preprocess_user_message(input_string):
    """
    Cleans and normalizes a user message by:
    - Removing emojis and non-ASCII characters
    - Decoding HTML entities
    - Normalizing Unicode text
    - Removing special characters (preserving currency and question mark)
    - Replacing multiple spaces with a single space
    - Lowercasing the string

    Args:
        input_string (str): The user message.

    Returns:
        str: Preprocessed and cleaned message.
    """

    if not input_string or not isinstance(input_string, str):
        return ""

    input_string = html.unescape(input_string)

    input_string = unicodedata.normalize('NFKC', input_string)

    input_string = re.sub(r"[^a-zA-Z0-9\s$€£¥₹?]", " ", input_string)

    input_string = re.sub(r"\s+", " ", input_string).replace("??", "?").strip()

    return input_string
