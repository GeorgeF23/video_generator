from html import unescape
import pdb
from typing import List
from bs4 import BeautifulSoup

def remove_html(content: str) -> List[str]:
    bs = BeautifulSoup(content, features="html.parser")
    paragraphs = bs.find_all('p')
    return list(map(lambda p: p.text, paragraphs))

def beautify(content: str) -> str:
    operations = [unescape, unescape, remove_html]

    for op in operations:
        content = op(content)
    return content