from database import *
import hashlib
import requests
import logging
import connexion
import json
from connexion.decorators.decorator import ResponseContainer
from flask import redirect, url_for, session, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user


# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


# POST Methods
def post_user():
    logging.debug('{Business} BEGIN function post_user()')
    name = connexion.request.form['name']
    email = connexion.request.form['email']
    password = connexion.request.form['passwordForm']
    logging.debug('{Business} Parameters: %s, %s, %s', name, email, password)
    if user_exists(email):
        logging.debug('{Business} END function post_user()')
        logging.info('{Business} Cant add user!!')
        return redirect(url_for('register'))
    sha = hashlib.sha1()
    sha.update(password)
    CRUD.create_user(name, email, sha.hexdigest())
    logging.debug('{Business} END function post_user()')
    logging.info('{Business} User added')
    return redirect(url_for('login'))


@login_required
def post_playlist():
    name = connexion.request.form['name']
    logging.debug('{Business} BEGIN function post_playlist()')
    logging.debug('{Business} Parameters: %s', name)
    CRUD.create_playlist(current_user, name)
    logging.debug('{Business} END function post_playlist()')
    logging.info('{Business} Playlist added')
    return redirect(url_for('post_playlist'))


@login_required
def post_song():
    title = connexion.request.form['title']
    artist = connexion.request.form['artist']
    album = connexion.request.form['album']
    release_year = connexion.request.form['releaseYear']
    logging.debug('{Business} BEGIN function post_song()')
    logging.debug('{Business} Parameters: %s, %, %, %', title, artist, album, release_year)
    CRUD.create_song(current_user, title, artist, album, release_year, "/path")
    logging.debug('{Business} END function post_song()')
    logging.info('{Business} Song added')
    return redirect(url_for('post_song'))


@login_required
def post_add_song_into_playlist():
    logging.debug('{Business} BEGIN function post_add_song_into_playlist()')
    playlist_id = connexion.request.args['id']
    song_id = session['addSongID']
    print playlist_id
    print song_id
    logging.debug('{Business} Parameters: %s, %s', playlist_id, song_id)
    playlist = CRUD.read_playlist(playlist_id)
    logging.debug('{Business} Playlist: %s', playlist)
    song = CRUD.read_song(song_id)
    logging.debug('{Business} Song: %s', song)
    playlist.songs.append(song)
    logging.debug('{Business} Changing playlist size to %s', playlist.size+1)
    CRUD.update_playlist(playlist, size=playlist.size+1)
    logging.debug('{Business} END function post_add_song_into_playlist()')
    logging.info('{Business} Song added to playlist')
    session.pop('addSongID', None)
    return redirect(url_for('post_playlist'))


@login_required
def post_remove_song_from_playlist():
    logging.debug('{Business} BEGIN function post_remove_song_from_playlist()')
    playlist_id = session['playSongID']
    song_id = connexion.request.args['idSong']
    logging.debug('{Business} Parameters: %s, %s', playlist_id, song_id)
    playlist = CRUD.read_playlist(playlist_id)
    logging.debug('{Business} Playlist: %s', playlist)
    for song in playlist.songs:
        if song_id == str(song.id):
            playlist.songs.remove(song)
    logging.debug('{Business} Changing playlist size to %s', playlist.size - 1)
    CRUD.update_playlist(playlist, size=playlist.size - 1)
    logging.debug('{Business} END function post_remove_song_from_playlist()')
    logging.info('{Business} Song removed from playlist')
    session.pop('playSongID', None)
    return redirect(url_for('post_playlist'))


# PUT Methods
@login_required
def put_user():
    logging.debug('{Business} BEGIN function put_user()')
    name = connexion.request.form['name']
    email = connexion.request.form['email']
    password = connexion.request.form['passwordForm']
    logging.debug('{Business} Parameters: %s, %s, %s', name, email, password)
    logging.debug('{Business} User: %s', current_user)
    if name == "":
        name = None
    if email == "":
        email = None
    if password == "":
        password = None
    CRUD.update_user(current_user, name, email, password)
    logging.debug('{Business} END function put_user()')
    logging.info('{Business} User updated')
    return redirect(url_for('home'))


@login_required
def put_playlist():
    playlist_id = session['playID']
    name = connexion.request.form['name']
    logging.debug('{Business} BEGIN function put_playlist()')
    logging.debug('{Business} Parameters: %s, %s', playlist_id, name)
    playlist = CRUD.read_playlist(playlist_id)
    logging.debug('{Business} Playlist: %s', playlist)
    if name == "":
        name = None
    CRUD.update_playlist(playlist, name=name)
    logging.debug('{Business} END function put_playlist()')
    logging.info('{Business} Playlist updated')
    return redirect(url_for('post_playlist'))


@login_required
def put_song():
    song_id = session['songID']
    title = connexion.request.form['title']
    artist = connexion.request.form['artist']
    album = connexion.request.form['album']
    release_year = connexion.request.form['release_year']
    if title == "":
        title = None
    if artist == "":
        artist = None
    if album == "":
        album = None
    if release_year == "":
        release_year = None
    logging.debug('{Business} BEGIN function put_song()')
    logging.debug('{Business} Parameters: %s, %s, %s, %s, %s', song_id, title, artist, album, release_year)
    song = CRUD.read_song(song_id)
    logging.debug('{Business} Song: %s', song)
    CRUD.update_song(song, title, artist, album, release_year, None)
    logging.debug('{Business} END function put_song()')
    logging.info('{Business} Song updated')
    return redirect(url_for('post_song'))


# GET Methods
@login_required
def get_user():
    logging.debug('{Business} BEGIN function get_user()')
    logging.debug('{Business} User: %s', current_user)
    logging.debug('{Business} END function get_user()')
    return current_user.dump()


@login_required
def get_user_playlists():
    logging.debug('{Business} BEGIN function get_user_playlists()')
    playlists = current_user.playlists
    asc = connexion.request.args['asc']
    logging.debug('{Business} Asc: %s', asc)
    if asc == "1":
        playlists.sort(key=lambda x: x.name, reverse=False)
    if asc == "2":
        playlists.sort(key=lambda x: x.name, reverse=True)
    if asc == "3":
        playlists.sort(key=lambda x: x.size, reverse=False)
    if asc == "4":
        playlists.sort(key=lambda x: x.size, reverse=True)
    if asc == "5":
        playlists.sort(key=lambda x: x.creation_date, reverse=False)
    if asc == "6":
        playlists.sort(key=lambda x: x.creation_date, reverse=True)
    logging.debug('{Business} END function get_user_playlists()')
    logging.info('{Business} Playlists retrieved')
    return [p.dump() for p in playlists]


@login_required
def get_playlist():
    logging.debug('{Business} BEGIN function get_playlist()')
    playID = session['playID']
    logging.debug('{Business} Parameters: %s', playID)
    playlist = CRUD.read_playlist(playID)
    logging.debug('{Business} END function get_playlist()')
    logging.info('{Business} Playlist retrieved')
    return playlist.dump()


@login_required
def get_song():
    logging.debug('{Business} BEGIN function get_song()')
    songID = session['songID']
    logging.debug('{Business} Parameters: %s', songID)
    song = CRUD.read_song(songID)
    logging.debug('{Business} END function get_song()')
    logging.info('{Business} Song retrieved')
    return song.dump()


@login_required
def get_playlist_songs():
    logging.debug('{Business} BEGIN function get_playlist_songs()')
    playlist_id = session["playSongID"]
    logging.debug('{Business} Parameters: %s', playlist_id)
    playlist = CRUD.read_playlist(playlist_id)
    logging.debug('{Business} Playlist: %s', playlist)
    songs = playlist.songs
    logging.debug('{Business} END function get_playlist_songs()')
    logging.info('{Business} Songs retrieved')
    return [p.dump() for p in songs]


@login_required
def get_user_songs():
    logging.debug('{Business} BEGIN function get_user_songs()')
    songs = current_user.songs
    for i in songs:
        if i.is_deleted == 1:
            songs.remove(i)
    logging.debug('{Business} END function get_user_songs()')
    logging.info('{Business} Songs retrieved')
    return [p.dump() for p in songs]


@login_required
def get_songs_criteria():
    logging.debug('{Business} BEGIN function get_songs_criteria()')
    title = session['title']
    artist = session['artist']
    logging.debug('{Business} Parameters: %s, %s', title, artist)
    if title == "":
        title = None
    if artist == "":
        artist = None
    songs = CRUD.read_songs_criteria(title, artist)
    logging.debug('{Business} END function get_songs_criteria()')
    logging.info('{Business} Songs retrieved')
    return [p.dump() for p in songs]


# DELETE Methods
@login_required
def delete_user():
    logging.debug('{Business} BEGIN function delete_user()')
    logging.debug('{Business} User: %s', current_user)
    for playlist in current_user.playlists:
        logging.debug('{Business} Deleting playlist: %s', playlist)
        CRUD.delete_something(playlist)
    admin = CRUD.read_user(email='admin')
    for song in current_user.songs:
        logging.debug('{Business} Changing song user: %s', song)
        song.user = admin
        CRUD.update_song(song)
    logging.debug('{Business} Deleting user: %s', current_user)
    CRUD.delete_something(current_user)
    logging.debug('{Business} END function delete_user()')
    logging.info('{Business} User deleted')
    return redirect(url_for('login'))


@login_required
def delete_song():
    logging.debug('{Business} BEGIN function delete_song()')
    song_id = connexion.request.args["id"]
    logging.debug('{Business} Parameters: %s', song_id)
    song = CRUD.read_song(song_id)
    logging.debug('{Business} Deleting song: %s', song)
    CRUD.delete_song(song)
    logging.debug('{Business} END function delete_song()')
    logging.info('{Business} Song deleted')
    return redirect(url_for('post_song'))


@login_required
def delete_playlist():
    logging.debug('{Business} BEGIN function delete_playlist()')
    playlist_id = connexion.request.args['id']
    logging.debug('{Business} Parameters: %s', playlist_id)
    playlist = CRUD.read_playlist(playlist_id)
    logging.debug('{Business} Deleting playlist: %s', playlist)
    CRUD.delete_something(playlist)
    logging.debug('{Business} END function delete_playlist()')
    logging.info('{Business} Playlist deleted')
    return redirect(url_for('post_playlist'))


# OTHER Methods
def user_exists(email):
    logging.debug('{Business} BEGIN function user_exists()')
    logging.debug('{Business} Checking email: %s', email)
    user = CRUD.read_user(email=email)
    logging.debug('{Business} END function user_exists()')
    if user is None:
        logging.info('{Business} No users found with the same email!!')
        return False
    logging.info('{Business} Email already in use!!')
    return True


def check_login():
    logging.debug('{Business} BEGIN function check_login()')
    email = connexion.request.form['email']
    password = connexion.request.form['password']
    logging.debug('{Business} Parameters: %s, %s', email, password)
    sha = hashlib.sha1()
    sha.update(password)
    user = CRUD.read_user(email=email, password=sha.hexdigest())
    logging.debug('{Business} END function check_login()')
    if user is None:
        logging.info('{Business} Login failed!!')
        return redirect(url_for('login'))
    else:
        login_user(user)
        logging.info('{Business} Login successful!!')
        return redirect(url_for('home'))


@login_required
def logout():
    session.pop('title', None)
    session.pop('artist', None)
    session.pop('playID', None)
    session.pop('songID', None)
    logout_user()
    return redirect(url_for('login'))

#____________________--------------________________________----------------
#==========================================================================


@login_required
def home():
    print current_user
    resp = application.send_static_file('home.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


def login():
    resp = application.send_static_file('login.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def edit_account_view():
    resp = application.send_static_file('editAccount.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


def register():
    resp = application.send_static_file('register.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )



def my_songs():
    # resp = application.send_static_file('listMySongs.html')
    # return ResponseContainer(
    #     mimetype=resp.mimetype,
    #     data=resp.response,
    #     status_code=200,
    #     headers=resp.headers
    # )
    r = requests.get("http://localhost:5000/getSongs")
    # print r.content
    data = json.loads(r.content)
    return jsonify(data)

@login_required
def my_playlists():
    resp = application.send_static_file('listPlayLists.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def my_playlist_edit():
    session['playID'] = connexion.request.args['pID']
    print session['playID']
    resp = application.send_static_file('editPlayList.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def my_song_edit():
    session['songID'] = connexion.request.args['sID']
    print session['songID']
    resp = application.send_static_file('editSong.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def search_songs():
    resp = application.send_static_file('searchSongs.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def search_songs_post():
    session['title'] = connexion.request.form['title']
    session['artist'] = connexion.request.form['artist']
    resp = application.send_static_file('listSearchedSongs.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def my_playlist_songs():
    print "PRIMEIRO"
    session.pop('playSongID', None)
    print "SEGUNDO"
    session['playSongID'] = connexion.request.args['id']
    print "TERCEIRO"
    print session['playSongID']
    logging.debug('{Business} BEGIN function my_playlist_songs')
    logging.debug('{Business} BEGIN function my_playlist_songs*******************************')
    print "OLA"
    resp = application.send_static_file('listPlayListSongs.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def add_song_playlist():
    session['addSongID'] = connexion.request.args['sID']
    resp = application.send_static_file('listPlayListsToAdd.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def create_song_view():
    resp = application.send_static_file('uploadSong.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


@login_required
def create_playlist_view():
    resp = application.send_static_file('createPlayList.html')
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


def send_javascript(js_page_name):
    resp = connexion.send_from_directory('js', js_page_name)
    return ResponseContainer(
        mimetype=resp.mimetype,
        data=resp.response,
        status_code=200,
        headers=resp.headers
    )


# starting connexion
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app


# starting database
CRUD.create_tables()
CRUD.connect_database()


# config
application.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

#flask-login
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login"


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return CRUD.read_user(id=userid)


application.add_url_rule('/mySongs', view_func=post_song)
application.add_url_rule('/myPlayLists', view_func=post_playlist)
application.add_url_rule('/login', view_func=login)
application.add_url_rule('/register', view_func=register)
application.add_url_rule('/', view_func=home)



if __name__ == '__main__':
    app.run(port=8080)
