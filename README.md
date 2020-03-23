# ReadWiki-ZH

从中文Wiki Dump中提取**有效词条**并转换至文本文件或Markdown文件。  
**有效词条**： 非Template, Category, Wikipedia, File, Topic, Portal, MediaWiki, Draft, Help等类型词条，多个同义词保留其中一个词条。

### 1. 下载中文Wiki Dump

#### 1.1 Wget下载

```python
from readwiki.wiki_download import WIKIDownload

# 选择Dump Index及输出文件夹
archive = '20200220'
output_dir = './dump'
print('Downloading dump:', archive)

# 使用Wget下载Dump文件
downloader = WIKIDownload(output_dir)
xml_path, txt_path = downloader.run(archive, verbose=True)

print('Index txt:', txt_path)
print('Content xml:', xml_path)
```

#### 1.2 手动下载

https://dumps.wikimedia.org/zhwiki/

### 2. 提取有效词条至文件

```python
from readwiki.wiki_parse2doc import WIKIParse2Doc

# Dump文件地址
xml_path = './dump/zhwiki-20200220-pages-articles-multistream.xml.bz2'

# 提取前100个有效词条至TXT文件
WIKIParse2Doc(xml_path, './docs/words_txt').run(num=100)
# 提取前100个有效至Markdown文件
WIKIParse2Doc(xml_path, './docs/words_md', markdown=True).run(num=100)
```

设置```num=None```，提取全部有效词条。  
词条共```3430255```个，  有效词条```1098595```个。