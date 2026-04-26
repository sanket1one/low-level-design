"""
Aggregation:

- whole-part relationship

has-a relationship

whole-part relationship with loose ownnership


If a class contains other classes for logical grouping only without lifecycle ownership, it is an aggregation.


Playlist: 1<>---- * Song

Playlist is whole.
Song is a part  which can exist independently.

"""


class Professor:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
		
class Department:
    def __init__(self, name, professors):
        self.name = name
        self.professors = professors

    def print_professors(self):
        print(f"Professors in {self.name} Department:")
        for professor in self.professors:
            print(f"- {professor.get_name()}")

# Department groups Professor objects, but it does not create them. The professors are created externally and passed into the department's constructor.


# 5. Parctical Example: Music Library System


"""
A music library manages artists, songs, playlists, and users.
The relationships between these entities show how parts (songs) can be shared across multiple wholes (playlists), and how deleting a whole leaves its parts intact.
"""


# Song which is written by an artist
# song can be in playlist or library:

# end user have a playlist:
# All song consist in one library

"""
Artist: Idependent entity
Song: belong to an artist but can exist independently of any playlist
Playlist aggreates song object. 
User: aggregates multiple playlists object, deleting user's playlist doesn't delete the songs.
Library: hold all songs , independent of any playlist or user.




user 1<>----* Playlist
Playlist 1<>---* Song
Library 1<>---* Song
Song *----->1 artist

"""



class Artist:
    def __init__(self, name):
        self.name = name


class Song:
    def __init__(self, title: str, artist: Artist, duration: int):
        self.title = title
        self.artist = artist
        self.duration = duration
    
    def __str__(self):
        return f"{self.title} by {self.artist.name} ({self.duration}s)"
    
class Playlist:
    def __init__(self, name: str):
        self.name = name
        self.songs = []

    def add_song(self, song: Song):
        if song not in self.songs:
            self.songs.append(song)
    
    def remove_song(self, song: Song):
        if song in self.songs:
            self.songs.remove(song)
    
    def get_song_count(self):
        return len(self.songs)

    def total_duration(self):
        return sum(song.duration for song in self.songs)

class User:
    def __init__(self, name: str):
        self.name = name
        self.playlists = []
    
    def create_playlist(self, playlist_name: str):
        playlist = Playlist(playlist_name)
        self.playlists.append(playlist)
        return playlist

    def delete_playlist(self, playlist: Playlist):
        if playlist in self.playlists:
            self.playlists.remove(playlist)

class Library:
    def __init__(self):
        self.songs = []
    
    def add_song(self, song: Song):
        if song not in self.songs:
            self.songs.append(song)
    
    def remove_song(self, song: Song):
        if song in self.songs:
            self.songs.remove(song)