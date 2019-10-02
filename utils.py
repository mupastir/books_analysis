def get_variables():
    vars = {}
    with open('_input/variables.in', 'r') as v:
        for v in v.readlines():
            key, val = v.split("=")
            key = key.strip()
            val = val.replace('"', '').strip()
            vars[key] = val
    return vars


VARIABLES = get_variables()
