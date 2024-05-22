import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextBox
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

def song_exist_on_spotify(song: str) -> bool:
    client_id = '386fc7b518d34d03b9ce2b8ac5dd91ed'
    client_secret = 'cdd1e830b42c43039789df825344f0c1'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)

    if song.strip():
        results = spotify.search(q=song, type='track', limit=50)
        return any(item['name'].lower().strip() == song.lower().strip() for item in results['tracks']['items'])
    else:
        return False


# ->[str] means that the def must return an array of strings
def extract_text_from_pdf(pdf_file: str) -> [str]:
    italic_text = set()
    word = ""

    for page_layout in extract_pages(pdf_file):
        for element in page_layout:
            if isinstance(element, LTTextBox):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            if 'Italic' in character.fontname:
                                word += character.get_text()
                            else:
                                if word and len(word.strip()) > 1:
                                    italic_text.add(word)
                                word = ""
                    if word and len(word.strip()) > 1:
                        italic_text.add(word)

    return italic_text


if __name__ == '__main__':
    extracted_text = extract_text_from_pdf('TLQNF.pdf')
    for text in extracted_text:
        if song_exist_on_spotify(text):
            print(text)
