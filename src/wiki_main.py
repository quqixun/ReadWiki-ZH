from wiki_parse import WIKIParse
from wiki_download import WIKIDownload


# =====================================
# STEP 1 : DOWNLOAD WIKI DUMP
# =====================================

# DENPENDENCY: wget

archive = '20190801'
output_dir = '../data'
print('Downloading dump:', archive)

downloader = WIKIDownload(output_dir)
xml_path, txt_path = downloader.run(
    archive, verbose=True
)

print('Index txt:', txt_path)
print('Content xml:', xml_path)


# =====================================
# STEP 2 : PARSE XML TO HUMAN-READABLE
# =====================================

# xml_path = '../data/zhwiki-20190801-pages-articles-multistream.xml.bz2'

md_parser = WIKIParse(
    xml_path, save_as='md',
    output_dir='../data/words_md'
)
md_parser.run()

txt_parser = WIKIParse(
    xml_path, save_as='txt',
    output_dir='../data/words_txt'
)
txt_parser.run()
