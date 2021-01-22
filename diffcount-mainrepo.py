# Checks differences between eo-OO.txt and en-GB.txt TL files

import sys
import os
import re

# Generate dict of STR_[number] translations
# Example entry: '{STR_0100': {'en': '[English translation here]', 'eo': '[Esperanto translation here]'}}'
def generate_numbered_strings_dict(en_strings, eo_strings):
    numbered_str_dict = dict()
    def generate_tags_for_single_lang(strings, lang_tag):
        for line in strings:
            attempt_tag = line.split(':')
            if len(attempt_tag) <= 1:
                continue
            tag, entry = attempt_tag[0], ":".join(attempt_tag[1:]).strip()
            tag = tag.strip()
            tagtype, tagnum = tag.split('_')
            try:
                int(tagnum)
            except:
                continue
            if tagtype == 'STR':
                if tag not in numbered_str_dict:
                    numbered_str_dict[tag] = dict()
                numbered_str_dict[tag][lang_tag] = entry

    generate_tags_for_single_lang(en_strings, 'en')
    generate_tags_for_single_lang(eo_strings, 'eo')
    return numbered_str_dict

# Returns whether the string is just template
template_re = re.compile(r'(\W*(\{[^\}]*\})?(\W*|( x )))+|[^A-Za-z]+')
def is_template(entry):
    return len(entry.strip()) == 0 or template_re.fullmatch(entry.strip()) is not None

# Checks EO translation quality and notes any empty strings
def main(args):
    dirname = os.path.dirname(__file__)
    langdir = os.path.join(dirname, '../OpenRCT2-localization/data/language')

    print('Reminder: visit https://raw.githubusercontent.com/OpenRCT2/OpenRCT2/develop/data/language/en-GB.txt for latest en-GB.txt')

    with open(os.path.join('en-GB.txt'), 'r') as f:
        eng_lines = f.readlines()

    compare_file = args[1] if len(args) == 2 else 'eo-OO.txt'
    with open(os.path.join(langdir, compare_file), 'r') as f:
        eo_lines = f.readlines()

    diff_counter = 0
    total_counter = 0
    template_strings = 0

    ref_dict = generate_numbered_strings_dict(eng_lines, eo_lines)
    for tag, tls in ref_dict.items():
        if 'en' in tls and not 'eo' in tls:
            print('Not yet translated: ' + tag)
        elif 'eo' in tls and not 'en' in tls:
            print("Not in en-GB vers.: " + tag)

    for tag, entry in ref_dict.items():
        total_counter += 1
        if 'en' not in entry or 'eo' not in entry:
            continue
        is_template_str = is_template(entry['en'])
        if entry['en'] != entry['eo']:
            if not is_template_str:
                diff_counter += 1
            else:
                print(f"Warning: {tag} seems to be translated template: original {entry['en']} vs translated {entry['eo']}")
        else:
            if is_template_str:
                template_strings += 1
            else:
                print(f"Warning: {tag} has same value as en-GB version: {entry['en']}")

    print(f'{diff_counter} lines are different')
    print(f'{total_counter} lines in total')
    print(f'{int((diff_counter+template_strings)/total_counter*100)}% of STR_[number] lines translated')
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv)