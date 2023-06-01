import re


def get_tool(t):
    action = None
    regex = r"ツール選択[: |：].*?\[(.*?)\].*?[\n]+"
    match = re.search(regex, t, re.DOTALL)
    if match:
        action = match.group(1)

    action_input = None
    regex = r"ツールへの入力[: |：](.*?)[\n]+"
    match = re.search(regex, t, re.DOTALL)
    if match:
        action_input = match.group(1)

    return action, action_input

def get_final_answer(t):
    regex = r"最終的な答え[: |：](.*?)[\n]+"
    match = re.search(regex, t, re.DOTALL)
    if match:
        result = match.group(1)
        return result
    return None