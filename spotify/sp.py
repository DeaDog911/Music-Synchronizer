import tekore as tk

from spotify.config import *


class SpotifyProfile:
    def __init__(self, client_id, client_secret, redirect_url, user_id):
        conf = (client_id, client_secret, redirect_url)
        token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
        self.sp = tk.Spotify(token)
        self.user_id = user_id

    def get_playlist(self, playlist_id):
        return self.sp.playlist(playlist_id=playlist_id)

    def search_track(self, query):
        return self.sp.search(query, types=('track', ), limit=1)[0].items[0]

    def add_track_to_playlist(self, playlist_id, uris):
        self.sp.playlist_add(playlist_id, uris=uris)

    def get_playlists(self):
        dict = {}
        for playlist in self.sp.playlists(self.user_id).items:
            dict[playlist.id] = playlist.name
        return dict

    def get_tracks(self, playlist_id):
        return self.sp.playlist(playlist_id).tracks

    def get_playlist_id(self, playlist_name):
        """
        :param playlist_name:
        :return: If playlist with this name exist, then returns playlist's id. If not, returns None
        """
        for playlist in self.sp.playlists(self.user_id).items:
            if playlist_name == playlist.name:
                return playlist.id
        else:
            return None

    def track_in_playlist(self, track, playlist_id) -> bool:
        tracks = self.get_tracks(playlist_id)
        if track in tracks.items:
            return True
        else:
            return False