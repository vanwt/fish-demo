def parser_cookie(cookie):
    data = {}
    for c in cookie.split(";"):
        key, *value = c.strip().split("=")
        if '[' in value and ']' in value or "{" in value and "}" in value:
            value = eval(value.replace("null", "None").replace("undefined", "None"))
            data.update(value)
        else:
            data.update({key: value})

    return data
