import os

from tqdm import tqdm
from wiki_parse import WIKIParse


class WIKIParse2Doc(WIKIParse):

    def __init__(
        self, input_file, output_dir, as_md=False
    ):

        super(WIKIParse2Doc, self).__init__(
            input_file, as_md
        )

        try:
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
        except Exception as e:
            raise ValueError(e)
        self.output_dir = output_dir

        return

    def __to_file(self, ID, text):

        text_file = ID + '.md' if self.as_md \
            else ID + '.txt'

        text_output_path = os.path.join(
            self.output_dir, text_file
        )
        with open(text_output_path, 'w',
                  encoding='utf-8') as file:
            file.write(text)

        return

    def run(self):

        n_iter = 0
        iter_wiki_content = tqdm(
            self.wiki_content,
            desc='Articls parsed: 0'
        )

        for content in iter_wiki_content:
            ID, text = self.parse(content)
            if ID is None:
                continue

            self.__to_file(ID, text)

            n_iter += 1
            if n_iter % 1000 == 0:
                iter_wiki_content.set_description(
                    'Articls parsed: {}'.format(n_iter)
                )

            if n_iter == 1:
                break

        return
