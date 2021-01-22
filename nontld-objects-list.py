# Lists number of untranslated strings in object files by letter

import sys
import os
import json

verbose = 1

def main():
    dirname = os.path.dirname(__file__)
    langdir = os.path.join(dirname, '../OpenRCT2-localization')

    with open(os.path.join(langdir, 'objects/eo-OO.json'), 'r') as f:
        eo_text = f.read()
        eo_json = json.loads(eo_text)

    # untranslated_by_letter: { [letter]: [count] }
    # e.g. untranslated_by_letter['A'] = 3
    # 'letter' '0' is used for strings that don't start with a letter
    untranslated_by_letter = dict({ '0': 0 })
    for i in range(ord('A'), ord('Z') + 1):
        untranslated_by_letter[str(chr(i))] = 0

    def check_field(datakey, tag, data):
        if datakey in data:
            to_print = data['reference-' + datakey]
            if to_print == data[datakey] and len(to_print) > 0:
                letter = data['reference-name'][0].upper()
                if letter < 'A' or letter > 'Z':
                    letter = '0'
                untranslated_by_letter[letter] += 1
                if verbose:
                    print(to_print)

    for tag, data in eo_json.items():
        check_field('name', tag, data)
        check_field('description', tag, data)
        check_field('capacity', tag, data)
    
    for letter, data in untranslated_by_letter.items():
        print(f"{letter} has {data} untranslated entries.")

    sys.exit(0)

if __name__ == '__main__':
    main()
