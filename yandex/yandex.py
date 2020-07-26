from utils.utils import make_request
import csv


class YandexProfile:
    def __init__(self, ya_user_id):
        self.ya_user_id = ya_user_id

    def get_playlist(self, kinds):
        url = f'https://music.yandex.ru/handlers/playlist.jsx?owner={self.ya_user_id}&kinds={kinds}'
        ya_response = make_request(url).json()
        return ya_response['playlist']

    def get_liked_playlist(self):
        # Плейлист "Мне нравиться"
        kinds = 3
        ya_playlist = self.get_playlist(kinds)
        return ya_playlist


class YandexTrack:
    def __init__(self, track):
        self.track = track

    def get_track_id(self):
        return self.track["id"]

    def get_track_title(self):
        return self.track['title']

    def get_track_artists(self):
        try:
            artists_str = ', '.join(artist['name'] for artist in self.track['artists'])
        except Exception:
            artists_str = ''
            print(Exception)
        return artists_str

    def get_track_info(self):
        return [
            self.get_track_id(),
            self.get_track_title(),
            self.get_track_artists(),
        ]


class YandexPlaylist:
    def __init__(self, playlist):
        self.playlist = playlist
        self.tracks = playlist['tracks']

    def get_tracks(self):
        return self.tracks

    def get_length(self):
        return len(self.tracks)

    def write_tracks(self, filename='tracks.csv'):
        try:
            with open(filename, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'title', 'artists'])
                for track in self.tracks:
                    track = YandexTrack(track)
                    try:
                        writer.writerow(track.get_track_info())
                    except UnicodeEncodeError:
                        continue
        except Exception:
            print(Exception)
