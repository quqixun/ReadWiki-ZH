from readwiki.wiki_download import WIKIDownload
from readwiki.wiki_parse2doc import WIKIParse2Doc


# =====================================
# STEP 1 : DOWNLOAD WIKI DUMP
# =====================================

# DENPENDENCY: wget

archive = '20200220'
output_dir = './dump'
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

# xml_path = '../dump/zhwiki-20190820-pages-articles-multistream.xml.bz2'

# WIKIParse2Doc(xml_path, '../docs/words_txt').run()
# WIKIParse2Doc(xml_path, '../docs/words_md', as_md=True).run()
