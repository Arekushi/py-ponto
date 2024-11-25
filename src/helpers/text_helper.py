def split_text_by_limit(text, limit=2000):
    parts = []
    start = 0

    while start < len(text):
        end = min(start + limit, len(text))
        
        newline_pos = text.rfind('\n', start, end)
        if newline_pos == -1:
            newline_pos = end

        parts.append(text[start:newline_pos].strip())

        start = newline_pos + 1

    return parts
