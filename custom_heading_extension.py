from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree import ElementTree as etree

class CustomHeadingTreeprocessor(Treeprocessor):
    def run(self, root):
        for elem in root.iter():
            if elem.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                header_level = int(elem.tag[1])
                elem.set('class', f'header{header_level}')

class CustomHeadingExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(CustomHeadingTreeprocessor(md), 'customheading', 176)
