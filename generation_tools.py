# Extracts elements the player can interact with from a text
def extract_elements(description, element_name):
    start_index = description.find(f"{element_name} = [")
    end_index = description.find("]", start_index)

    if start_index != -1 and end_index != -1:
        elements_str = description[start_index + len(f"{element_name} = ["):end_index]
        elements = [elem.strip("'\" ") for elem in elements_str.split(",")]
        return elements
    else:
        return []


# Extracts actions and their associated characteristics from a text
def extract_actions_and_characteristics(description):
    start_index = description.find("actions = [")
    end_index = description.find("]", start_index)

    actions_with_characteristics = []

    if start_index != -1 and end_index != -1:
        actions_str = description[start_index + len("actions = ["):end_index]
        actions_list = [action.strip("'\" ") for action in actions_str.split(",")]

        for action in actions_list:
            if "(" in action and ")" in action:
                action_text, characteristic = action.rsplit("(", 1)
                characteristic = characteristic.rstrip(")")
                actions_with_characteristics.append((action_text.strip(), characteristic.strip()))

    return actions_with_characteristics