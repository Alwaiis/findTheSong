import re
from typing import Any

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextBox
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


def create_playlist_and_add_songs(username: str, playlist_name: str, song_ids: list[str]) -> None:
    scope = "playlist-modify-public"
    client_id = '386fc7b518d34d03b9ce2b8ac5dd91ed'
    client_secret = 'cdd1e830b42c43039789df825344f0c1'
    redirect_uri = 'http://localhost:8888/callback'  # This should be replaced with your redirect URI

    token = SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    spotify = spotipy.Spotify(auth_manager=token)

    # Create a new playlist
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=True)
    playlist_id = playlist['id']

    # Add songs to the playlist
    spotify.playlist_add_items(playlist_id, song_ids)


def song_exist_on_spotify(song: str) -> str | None:
    client_id = '386fc7b518d34d03b9ce2b8ac5dd91ed'
    client_secret = 'cdd1e830b42c43039789df825344f0c1'
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)

    if song.strip():
        results = spotify.search(q=song, type='track', limit=50)
        for item in results['tracks']['items']:
            if item['name'].lower().strip() == song.lower().strip():
                return item['id']
    return None


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
    name_of_pdf = input("Enter the name of the PDF file: ")

    extracted_text = extract_text_from_pdf(name_of_pdf)
    song_ids = set()  # Use a set to avoid duplicates
    for text in extracted_text:
        song_id = song_exist_on_spotify(text)
        if song_id is not None:
            song_ids.add(song_id)  # Add the song ID to the set
            print(text)
    # input("Enter your Spotify username: "))

    username = '31xbus24n7atxw4l7voszoquntae'
    playlist_name = name_of_pdf
    create_playlist_and_add_songs(username, playlist_name, list(song_ids))  # Convert the set to a list
