import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, redirect, request, session, url_for, render_template
import requests
import pandas as pd
import os
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'aaryans_secret_key'

client_id = ''
client_secret = ''
redirect_uri = "http://127.0.0.1:5000/callback"
scope = 'playlist-read-private'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    access_token = get_access_token(code)

    if access_token:
        session['access_token'] = access_token
        user_profile = fetch_user_profile(access_token)
        if user_profile:
            session['username'] = user_profile.get('display_name')
        playlists = fetch_playlists(access_token)
        return render_template('select_playlists.html',playlists=playlists)
    else:
        return "Failed to retrieve access token"
    
def get_access_token(code):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded' 
    }
    data = {
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : redirect_uri,
        'client_id' : client_id,
        'client_secret' : client_secret 
    }

    response = requests.post(url, headers= headers, data=data)
    response_data = response.json()
    return response_data.get('access_token')

def fetch_user_profile(access_token):
    url = "https://api.spotify.com/v1/me"
    headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code ==200:
        return response.json()
    else:
        return None
    
def fetch_playlists(access_token):
    url = 'https://api.spotify.com/v1/me/playlists'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        playlists = response.json().get('items', [])
        playlist_info = []
        for playlist in playlists:
            playlist_info.append({
                'id': playlist['id'],         
                'name': playlist['name'],      
                'track_count': playlist['tracks']['total']  
            })
        return playlist_info
    else:
        print(f"Failed to fetch playlists. Status code: {response.status_code}")
        return []

@app.route('/fetch_songs', methods=['POST'])
def fetch_songs():
    selected_playlists = request.form.getlist('playlist_ids')
    access_token = session.get('access_token')

    all_songs = []
    playlist_names = []  
    
    for playlist_id in selected_playlists:
        playlist_details = fetch_playlists(access_token)
        playlist_name = next((playlist['name'] for playlist in playlist_details if playlist['id'] == playlist_id), None)
        
        if playlist_name:  
            playlist_names.append(playlist_name)
        
        songs = fetch_songs_from_playlist(access_token, playlist_id)
        all_songs.extend(songs)
    
    session['playlists'] = playlist_names  
    
    save_songs_to_csv(all_songs)
    return render_template("display_songs.html", songs=songs, username=session.get('username'), playlists=session.get('playlists'))

def fetch_songs_from_playlist(access_token,playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(url,headers=headers)
    tracks = response.json().get('items',[])

    songs = []
    for track in tracks:
        song_info = track.get('track')
        if not song_info:
            continue
        duration_ms = song_info.get('duration_ms', 0)
        minutes = (duration_ms // 1000) // 60
        seconds = (duration_ms // 1000) % 60
        added_at = track.get('added_at', 'Unknown')

        songs.append({
            'Song Name': song_info.get('name', 'Unknown'),
            'Artist Name': ', '.join([artist.get('name', 'Unknown') for artist in song_info.get('artists', [])]),
            'Album Name': song_info.get('album', {}).get('name', 'Unknown'),
            'Track URL': song_info.get('external_urls', {}).get('spotify', 'No URL'),
            'added_at' : added_at,
            'track_id': song_info.get('id', 'No ID'),
            'duration_formatted' : f"{minutes}:{seconds:02d}"
        })
    return songs

def save_songs_to_csv(songs,filename="songs.csv"):
    df = pd.DataFrame(songs)
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    app.run(debug=True)