# ReadWiki-ZH

从中文Wiki Dump中提取**有效词条**并转换至文本文件或Markdown文件。  
**有效词条**： 非Template, Category, Wikipedia, File, Topic, Portal, MediaWiki, Draft, Help等类型词条，多个同义词保留其中一个词条。

### 1. 环境配置

测试环境： Python 3.7.4， Ubuntu 18.04， Windows 7  
虚拟环境中安装依赖项
```
pip install -r requirements.txt
```

### 2. 下载中文Wiki Dump

#### 2.1 Wget下载

需安装`[Wget](https://www.gnu.org/software/wget/)。

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

#### 2.2 手动下载

在[中文Dump Index](https://dumps.wikimedia.org/zhwiki/)页面下选择一个归档日期。归档日期越新，包含的词条越多。  
选择```20200220```后(也可选择其他日期)，下载以下两个文件，并解压至[dump](./dump)文件夹。

```
zhwiki-20200220-pages-articles-multistream.xml.bz2 1.9 GB
zhwiki-20200220-pages-articles-multistream-index.txt.bz2 26.9 MB
```

### 3. 提取有效词条至文件

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
提取完成后，输出文件可在[docs](./docs)文件夹查看。  
几个输出示例：[数学](./docs/words_md/13.md)， [开放源代码](./docs/words_md/256.md)， [邓丽君](./docs/words_md/333.md)
