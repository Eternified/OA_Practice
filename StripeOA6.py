raw_query = "Status=success & type= refund & customer= & =anonymous & date=2026-10-24 & invalid_fragment"

def sanitize_query_string(query_str):
    if query_str is None or query_str == "":
        return {}

    sanitized_queries = {}
    fragments = query_str.split("&")

    for fragment in fragments:
        if "=" not in fragment:
            continue

        key, value = fragment.split("=", 1)

        cleaned_key = key.strip().lower()
        cleaned_value = value.strip()

        if cleaned_key != "" and cleaned_value != "":
            sanitized_queries[cleaned_key] = cleaned_value

    return sanitized_queries

print(sanitize_query_string(raw_query))