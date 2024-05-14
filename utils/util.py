def format_description(description: str):
    """
    This function gets the whole description and each 100 chars it appends an \n
    :param description: str
    :return: str
    """
    result = ''
    for index, char in enumerate(description):
        if index > 300:
            break
        result += char
        if not (index + 1) % 30:
            result += '\n'

    return result
