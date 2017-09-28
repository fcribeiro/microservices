from sqlalchemy import Table, Column, ForeignKey
from Base import Base

# association table
playlist_song = Table('playlist_song', Base.metadata,
                      Column('playlist.id', ForeignKey('playlists.id'), primary_key=True),
                      Column('song.id', ForeignKey('songs.id'), primary_key=True)
                      )

