import re
import bz2file

from opencc import OpenCC
from gensim.corpora.wikicorpus import (
    extract_pages, filter_wiki
)


class WIKIParse(object):

    KEYWORDS = [
        'Template', 'Category', 'Wikipedia',
        'File', 'Topic', 'Portal',
        'MediaWiki', '模块', 'Draft', 'Help'
    ]

    def __init__(self, input_file, as_md=False):
        try:
            bz2_file = bz2file.open(input_file)
            self.wiki_content = extract_pages(bz2_file)
        except Exception as e:
            raise RuntimeError(e)

        self.as_md = as_md
        self.opencc = OpenCC('t2s')
        self.nl = '\n\n' if as_md else '\n'
        return

    def __is_not_word(self, word):
        word_items = word.split(':')
        if len(word_items) > 1 and \
                word_items[0] in self.KEYWORDS:
            return True
        return False

    def __is_redirect(self, text):
        return re.findall(r'^#', text)

    def __clean_synonym(self, s):
        t1 = r'-{(.*?)}-'
        t2 = r'.*zh-(?:hans|cn):(.*?)(;|}-|;zh).*'

        while True:
            match1 = re.search(t1, s, re.DOTALL)
            if match1 is None:
                break

            start, end = match1.span()
            sub_s = s[start:end].replace(' ', '')
            match2 = re.match(t2, sub_s, re.DOTALL)

            if match2 is not None:
                sub_s = match2.group(1)
            else:
                sub_s = sub_s[2:-2]
                if 'zh-hans' in sub_s or 'zh-cn' in sub_s:
                    sub_s = ''

            s = s[:start] + sub_s + s[end:]
        return s

    def __clean_template(self, s):
        t = r'{{(?!lang)(.*?)}}'

        while True:
            match = re.search(t, s)
            if match is None:
                break

            start, end = match.span()
            s = s[:start] + s[end:]
        return s

    def __clean(self, s):
        s = self.__clean_synonym(s)
        # s = self.__clean_template(s)

        s = re.sub(r':*{\|[\s\S]*?\|}', '', s)
        s = re.sub(r'\[\[File:.*\]\]', '', s)
        s = re.sub(r'<gallery[\s\S]*?</gallery>', '', s)
        s = re.sub(r'(.){{([^{}\n]*?\|[^{}\n]*?)}}',
                   '\\1[[\\2]]', s)
        s = filter_wiki(s)
        s = re.sub(r'\* *\n|\'{2,}', '', s)
        s = re.sub('\n+', '\n', s)
        s = re.sub('\n[:;]|\n +', '\n', s)
        s = re.sub('\n==', '\n\n==', s)
        s = s.replace('\n。', '。\n')
        return s

    def __fresh(self, word, text):
        def update(cn):
            return str(int(cn) + 1)

        def get_title(line, symbol):
            temp = '{}(.+?){}'.format(symbol, symbol)
            match = re.search(temp, line)
            if match is None:
                return ''

            title = match.group(1)
            title = title.strip()
            return title

        def form_line(catalog, title, level):
            if catalog:
                level = len(catalog) - catalog.count('0') + 1
                catalog = [c for c in catalog if c != '0']
                line = '.'.join(catalog) + ' ' + title
            else:
                line = title + self.nl

            if self.as_md:
                line = '#' * level + ' ' + line
            return line

        fresh_text = form_line(None, word, 1)
        prev_item_line = False
        c2, c3, c4, c5 = '0', '0', '0', '0'
        for line in text.split('\n'):
            item_line = False
            if line.startswith('====='):
                c5 = update(c5)
                title = get_title(line, '=====')
                line = form_line([c2, c3, c4, c5], title, 5)
            elif line.startswith('===='):
                c4, c5 = update(c4), '0'
                title = get_title(line, '====')
                line = form_line([c2, c3, c4], title, 4)
            elif line.startswith('==='):
                c3, c4, c5 = update(c3), '0', '0'
                title = get_title(line, '===')
                line = form_line([c2, c3], title, 3)
            elif line.startswith('=='):
                c2, c3, c4, c5 = update(c2), '0', '0', '0'
                title = get_title(line, '==')
                line = form_line([c2], title, 2)
            elif line.startswith('***'):
                line = '  * ' + line[3:].strip()
                item_line, prev_item_line = True, True
            elif line.startswith('**'):
                line = ' * ' + line[2:].strip()
                item_line, prev_item_line = True, True
            elif line.startswith('*') or line.startswith('#'):
                line = '* ' + line[1:].strip()
                item_line, prev_item_line = True, True
            else:
                pass

            if not item_line and prev_item_line:
                fresh_text += '\n'
                prev_item_line = False

            nl = '\n' if item_line else self.nl
            fresh_text += line + nl
        return fresh_text

    def parse(self, content):
        word, text, ID = content

        if self.__is_not_word(word) or \
           self.__is_redirect(text):
            return None, None

        text = self.__clean(text)
        word = self.opencc.convert(word)
        text = self.opencc.convert(text)
        text = self.__fresh(word, text)

        return ID, text
