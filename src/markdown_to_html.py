from block_markdown import *
from htmlnode import *
from inline_markdown import *
from textnode import *


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div = ParentNode("div", [])
    for block in blocks:
        div.children.append(block_to_html_node(block, block_to_block_type(block)))
    return div

def text_to_children(text):
    list_of_text_nodes = text_to_textnodes(text)
    new_list = []
    for node in list_of_text_nodes:
        new_list.append(text_node_to_html_node(node))
    return new_list

def block_to_html_node(text, block_type):
    match block_type:
        case BlockType.QUOTE:
            return ParentNode("blockquote",text_to_children(text[1:].strip()))
        case BlockType.HEADING:
            i = 0
            for ch in text:
                if ch == "#":
                    i += 1
                else:
                    break
            clean_text = text[i:].strip()        
            return ParentNode(f"h{i}", text_to_children(clean_text))
        case BlockType.PARAGRAPH:
            clean_text = text.replace("\n", " ")
            return ParentNode("p", text_to_children(clean_text))
        case BlockType.CODE:
            lines = text.split("\n")
            start_idx = 0
            for i, line in enumerate(lines):
                if line.strip() == "```":
                    start_idx = i + 1
                    break
            
            end_idx = len(lines)
            for i in range(len(lines)-1, -1, -1):
                if lines[i].strip() == "```":
                    end_idx = i
                    break
            
            code_content = "\n".join(lines[start_idx:end_idx])
            if not code_content.endswith("\n"):
                code_content += "\n"
            
            text_node = TextNode(code_content, TextType.TEXT)
            code_html = text_node_to_html_node(text_node)
            return ParentNode("pre", [ParentNode("code", [code_html])])
        case BlockType.ULIST:
            ul = ParentNode("ul", [])
            split_text = text.split("\n")
            for line in split_text:
                if not line.strip():
                    continue
                clean_line = line[2:].strip()
                ul.children.append(ParentNode("li", text_to_children(clean_line)))
            return ul
        case BlockType.OLIST:
            ol = ParentNode("ol", [])
            split_text = text.split("\n")
            for line in split_text:
                if not line.strip():
                    continue
                dot_space_index = line.find(". ")
                if dot_space_index != -1:
                    clean_line = line[dot_space_index + 2:].strip()
                    ol.children.append(ParentNode("li", text_to_children(clean_line)))
            return ol
        
def extract_title(markdown):
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title_start = "<h1>"
    title_end = "</h1>"
    if title_start in html:
        first_split = html.split(title_start, 1)
        second_split = (first_split[1].split(title_end, 1))
        return second_split[0]
    else:
        raise Exception("No <h1> header in markdown")