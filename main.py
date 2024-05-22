import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextBox


# ->[str] means that the def must return an array of strings
def extract_text_from_pdf(pdf_file: str)-> [str]:
        italic_text = []

        for page_layout in extract_pages(pdf_file):
            for element in page_layout:
                if isinstance(element, LTTextBox):
                    for text_line in element:
                        word = ""
                        for character in text_line:
                            if isinstance(character, LTChar):
                                if 'Italic' in character.fontname:
                                    word += character.get_text()
                        if word:
                            italic_text.append(word)

        return italic_text


if __name__ == '__main__':
    extracted_text = extract_text_from_pdf('TLQNF.pdf')
    for text in extracted_text:
        print(text)
