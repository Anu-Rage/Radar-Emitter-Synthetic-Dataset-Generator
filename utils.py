def parse_input_list(input_text):

    if not input_text.strip():
        return []

    return [
        float(x.strip())
        for x in input_text.split(",")
        if x.strip()
    ]