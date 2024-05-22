import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextBox
from Song_List import SongList
import requests

def song_exist_on_deezer(song: str) -> bool:
    response = requests.get(f'https://api.deezer.com/search?q={song}')
    data = response.json()
    if 'data' in data:
        return len(data['data']) > 0
    else:
        print(" ")
        return False
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
                        if word and len(word.strip()) > 1:
                            italic_text.append(word)

        return italic_text


if __name__ == '__main__':
    extracted_text = extract_text_from_pdf('TLQNF.pdf')
    for text in extracted_text:
        if song_exist_on_deezer(text):
            print(text)
