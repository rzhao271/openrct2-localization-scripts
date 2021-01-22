# Checks differences between eo-OO.json and en-GB.json object files

import sys
import os
import json

print_not_translated = False

def main():
    dirname = os.path.dirname(__file__)
    langdir = os.path.join(dirname, '../OpenRCT2-localization')

    with open(os.path.join(langdir, 'objects/eo-OO.json'), 'r') as f:
        eo_text = f.read()
        eo_json = json.loads(eo_text)

    with open(os.path.join(langdir, 'objects/en-GB.json'), 'r') as f:
        original_text = f.read()
        original_json = json.loads(original_text)

    counters = {'diff': 0, 'total': 0}

    def check_field(datakey, tag, data):
        if datakey in data:
            counters['total'] += 1
            if data['reference-' + datakey] != data[datakey]:
                if len(data[datakey]):
                    counters['diff'] += 1
            else:
                if print_not_translated:
                    print(f'{datakey} for {tag} not translated')

    for tag, data in eo_json.items():
        check_field('name', tag, data)
        check_field('description', tag, data)
        check_field('capacity', tag, data)

    for tag, data in original_json.items():
        if tag not in eo_json:
            print(f"{tag} NOT IN TRANSLATED JSON BUT IN ORIGINAL")
            sys.exit(1)
        for datakey in data:
            if datakey not in eo_json[tag]:
                print(f"{datakey} for {tag} NOT IN TRANSLATED JSON BUT IN ORIGINAL")
                sys.exit(1)
        translated_data = eo_json[tag]
        for key, val in translated_data.items():
            if key.startswith('reference-') and val != original_json[tag][key]:
                print(f"{key} for {tag} CHANGED!")
                sys.exit(1)

    for tag, data in eo_json.items():
        if tag not in original_json:
            print(f"{tag} NOT IN ORIGINAL JSON BUT IN TRANSLATED")
            sys.exit(1)
        for datakey in data:
            if datakey not in original_json[tag]:
                print(f"{datakey} for {tag} NOT IN ORIGINAL JSON BUT IN TRANSLATED")
                sys.exit(1)

    print(f"{counters['diff']} lines are different")
    print(f"{counters['total']} lines to translate in total")
    print(f"{counters['total'] - counters['diff']} lines left to translate")
    print(f"{int(counters['diff']/counters['total']*100)}% of strings translated")
    sys.exit(0)

if __name__ == '__main__':
    main()
