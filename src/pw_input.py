import os
import re

import f90nml

from io import StringIO

class PWNml:
    def __init__(self, nml):
        self.nml = nml
    def to_dict(self, obj):
        self.nml.todict()
    def update(self, obj):
        self.nml.patch(obj)
    def dump(self):
        f = StringIO()
        f90nml.write(self.nml, f)
        return f.getvalue()
    def __repr__(self):
        return self.dump()

class PWNmlParser:
    def parse(self, input_nml_str):
        f = StringIO(input_nml_str)
        self.nml = f90nml.read(f)
        return PWNml(self.nml)

class PWCard:
    def __init__(self, keyword, keyword_option):
        self.keyword = keyword
        self.keyword_option = keyword_option
        self.lines = []
    def read_line(self, line):
        line = line.strip()
        words = re.split(r'\s+', line)
        return words
    def push_line(self, line):
        self.lines.append(self.read_line(line))
    def dump_line(self, idx):
        return ' '.join(self.lines[idx])
    def dump_lines(self):
        return '\n'.join([self.dump_line(line_index) for line_index in range(len(self.lines))])
    def dump(self):
        if self.keyword_option is None:
            return '%s\n%s' % (self.keyword, self.dump_lines())
        else:
            return '%s %s\n%s' % (self.keyword, self.keyword_option, self.dump_lines())
    def __repr__(self):
        return 'Keyword: %s\nOption: %s\nLines:\n%s' % (self.keyword, self.keyword_option, self.dump_lines())
    
class PWCards:
    def __init__(self, cards):
        self.cards = cards
    def __getitem__(self, key):
        return self.get(key)
    def get(self, key):
        return next((card for card in self.cards if card.keyword == key), None)
    def dump(self):
        return '\n\n'.join([card.dump() for card in self.cards])

class PWCardParser:
    def __init__(self):
        self.card_is_open = False
        self.cards = []
        self.current_card = None

    def read_card_row(self, line):
        self.current_card.push_line(line)

    def start_card(self, line):
        self.card_is_open = True

        KEYWORD_REGEX = r'^\s*(?P<keyword>\S+)(\s+(?P<option>.*))?$'

        regex_result = re.search(KEYWORD_REGEX, line)
        keyword = regex_result.group('keyword')
        keyword_option = regex_result.group('option')

        self.cards.append(PWCard(keyword, keyword_option))
        self.current_card = self.cards[-1]

    def end_card(self):
        self.card_is_open = False

    def parse_line(self, line):
        if self.card_is_open and line == '':
            self.end_card()
        elif not self.card_is_open and line != '':
            self.start_card(line)
        elif self.card_is_open and line != '':
            self.read_card_row(line)
        else:
            pass

    def parse(self, card_str):
        for line in card_str.split('\n'):
            line = line.rstrip('\n')
            self.parse_line(line)
        return PWCards(self.cards)

class PWInput:
    def __init__(self, template_file_path):
        with open(template_file_path, encoding='utf8') as template_file:
            input_string = template_file.read()
        #idx = re.search(r'.*/\s+\n', input_string).span()[1]
        idx = input_string.rfind('/\n')
        namelist_str = input_string[:idx+1]
        cards_str = input_string[idx+1:]
        self.cards = PWCardParser().parse(cards_str)
        self.nml = PWNmlParser().parse(namelist_str)
    def dump(self):
        return '\n'.join([
            self.nml.dump(),
            self.cards.dump()
        ])
        
if __name__ == '__main__':
    print(PWInput('t.in').dump())