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