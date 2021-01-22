# Replace "" and '' with  “ ” and ‘ ’ and use ’ as apostrophe
import re

filename = '../Localisation/objects/zh-CN.json'


def get_file_lines():
    with open(filename, 'r') as f:
        file = f.readlines()
    return file


def write_file_lines(lines):
    with open(filename, 'w') as f:
        f.writelines(lines)


def maybe_switch_quotes(line, orig_quote, new_left_quote, new_right_quote):
    oq = orig_quote
    lq = new_left_quote
    rq = new_right_quote
    match = re.match(f"[^{oq}<]*({oq}[^{oq}]*{oq})[^{oq}>]*", line)
    while match and 'reference' not in line:
        curgroup = match.groups()[0]
        extract = curgroup[1:-1]
        line = line.replace(curgroup, f"{lq}{extract}{rq}", 1)
        match = re.match(f"[^{oq}<]*({oq}[^{oq}]*{oq})[^{oq}>]*", line)
    return line

def maybe_switch_apostrophes(line):
    if 'reference' not in line and '\'' in line:
        line = line.replace('\'', '’')
    return line

def main():
    lines = get_file_lines()
    new_lines = []
    for line in lines:
        # line = maybe_switch_quotes(line, "\"", "“", "”")
        line = maybe_switch_quotes(line, "\'", "‘", "’")
        line = maybe_switch_apostrophes(line)
        new_lines.append(line)
    write_file_lines(new_lines)


if __name__ == "__main__":
    main()
