from wiki_download import WIKIDownload
from wiki_parse2doc import WIKIParse2Doc


# =====================================
# STEP 1 : DOWNLOAD WIKI DUMP
# =====================================

# DENPENDENCY: wget

# archive = '20190820'
# output_dir = '../data'
# print('Downloading dump:', archive)

# downloader = WIKIDownload(output_dir)
# xml_path, txt_path = downloader.run(
#     archive, verbose=True
# )

# print('Index txt:', txt_path)
# print('Content xml:', xml_path)


# =====================================
# STEP 2 : PARSE XML TO HUMAN-READABLE
# =====================================

xml_path = '../data/zhwiki-20190801-pages-articles-multistream.xml.bz2'

# md_parser = WIKIParse(
#     xml_path, save_as='md',
#     output_dir='../data/words_md'
# )
# md_parser.run()

# txt_parser = WIKIParse(
#     xml_path, save_as='txt',
#     output_dir='../data/words_txt'
# )
# txt_parser.run()

# WIKIParse2Doc(xml_path, '../data/words_txt').run()
WIKIParse2Doc(xml_path, '../data/words_md', as_md=True).run()
