import re

def extract_card_block(lines, name, type_, slot):
    pattern = re.compile(
        rf'<CARD\s+[^>]*Name="{re.escape(name)}"[^>]*Type="{re.escape(type_)}"[^>]*Slot="{re.escape(slot)}"[^>]*>'
    )
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if pattern.search(line):
            start_idx = i
            break

    if start_idx == -1:
        return None  # Not found

    for j in range(start_idx + 1, len(lines)):
        if re.search(r'<CARD\s+[^>]*Name="', lines[j]):
            end_idx = j
            break

    if end_idx == -1:
        end_idx = len(lines)

    return lines[start_idx:end_idx]

def replace_card_block(dest_lines, name, type_, slot, new_block):
    pattern = re.compile(
        rf'<CARD\s+[^>]*Name="{re.escape(name)}"[^>]*Type="{re.escape(type_)}"[^>]*Slot="{re.escape(slot)}"[^>]*>'
    )
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(dest_lines):
        if pattern.search(line):
            start_idx = i
            break

    if start_idx == -1:
        return None  # Not found

    for j in range(start_idx + 1, len(dest_lines)):
        if re.search(r'<CARD\s+[^>]*Name="', dest_lines[j]):
            end_idx = j
            break

    if end_idx == -1:
        end_idx = len(dest_lines)

    return dest_lines[:start_idx] + new_block + dest_lines[end_idx:]
