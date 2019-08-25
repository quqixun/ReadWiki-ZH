import os
import subprocess


DEVNULL = open(os.devnull, 'w')


class WIKIDownload(object):

    DUMPS_WIKI = 'https://dumps.wikimedia.org/zhwiki'
    XML_BASIS = 'zhwiki-{}-pages-articles-multistream.xml.bz2'
    TXT_BASIS = 'zhwiki-{}-pages-articles-multistream-index.txt.bz2'
    COMMANDS = ['wget', '-O', None, None]

    def __init__(self, output_dir):

        self.output_dir = output_dir
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        return

    def __download(self, archive, type, verbose=True):

        basis = self.XML_BASIS if type == 'xml' else self.TXT_BASIS

        data_file_name = basis.format(archive)
        data_bz2_path = os.path.join(self.output_dir, data_file_name)
        self.COMMANDS[-2] = data_bz2_path
        self.COMMANDS[-1] = '/'.join([self.DUMPS_WIKI, archive, data_file_name])

        if verbose:
            subprocess.call(self.COMMANDS)
        else:
            subprocess.call(self.COMMANDS, stdout=DEVNULL,
                            stderr=subprocess.STDOUT)

        return data_bz2_path

    def run(self, archive, verbose=True):

        xml_bz2_path = self.__download(archive, 'xml', verbose)
        txt_bz2_path = self.__download(archive, 'txt', verbose)

        return xml_bz2_path, txt_bz2_path
