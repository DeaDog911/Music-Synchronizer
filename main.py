from spotify.sp import SpotifyProfile

from yandex.yandex import YandexProfile
from yandex.yandex import YandexPlaylist
from yandex.yandex import YandexTrack

from config import *


class MusicSynchronizer:
    def __init__(self, yandex_user_id, spotify_user_id, sp_config):
        self.sp = SpotifyProfile(sp_config['client_id'], sp_config["client_secret"], sp_config["redirect_url"], spotify_user_id)
        self.ya = YandexProfile(yandex_user_id)

    def synchronize_yandex_liked_to_spotify(self, sp_playlist_name):
        ya_playlist = YandexPlaylist(self.ya.get_liked_playlist())
        ya_tracks = ya_playlist.get_tracks()

        sp_playlist_id = self.sp.get_playlist_id(sp_playlist_name)

        for ya_track in ya_tracks:
            ya_track_obj = YandexTrack(ya_track)
            try:
                track = self.sp.search_track(f'{ya_track_obj.get_track_title()} {ya_track_obj.get_track_artists()}')
                if not self.sp.track_in_playlist(track, sp_playlist_id):
                    track_uri = track.uri
                    self.sp.add_track_to_playlist(sp_playlist_id, [track_uri])
            except IndexError:
                pass


def main():
    ms = MusicSynchronizer(yandex_user_id, spotify_user_id, sp_config={
        'client_id': client_id,
        "client_secret": client_secret,
        "redirect_url": redirect_url,
    })
    spotify_playlist_name = "Yandex Музыка"
    ms.synchronize_yandex_liked_to_spotify(spotify_playlist_name)


if __name__ == '__main__':
    main()
