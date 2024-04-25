import tiktoken
import re
import pandas as pd

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    # copied from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print(
            "Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print(
            "Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
    elif model == "gpt-4-0314":
        tokens_per_message = 3
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        num_tokens += len(encoding.encode(message.content))
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def _parse_code(content: str) -> str:
    code_regex = r"```(?:python)?\n([\s\S]*)```"
    match = re.search(code_regex, content)
    code = match.group(1)
    return code


def _pandas_dtype_str(df: pd.DataFrame) -> str:
    return " ".join([f"{col}({dtype})" for col, dtype in df.dtypes.items()])
def load_prompt(path):
    prompt = ""
    with open(path, "r") as f:
        prompt = f.read()
    return prompt

