import spotipy
import spotipy.oauth2 as oauth2

with open('creds.txt') as file:
    creds = file.readlines()
    cli_id = creds[1].rstrip('\n')
    cli_sec = creds[2].rstrip('\n')
    
auth = oauth2.SpotifyClientCredentials(
    client_id=cli_id,
    client_secret=cli_sec
)

token = auth.get_access_token()
spotify = spotipy.Spotify(auth=token)

features = spotify.track('https://open.spotify.com/track/1tm4Bl2E5RwTevOiBs4gtH?si=X7KuHtN6TQ6lZ15ijB4v4A')
print(features['artists'][0]['name'],features['name'])

response = spotify.playlist_items('https://open.spotify.com/playlist/2kUbABZX9A2m0b6fopyouM?si=7gk-1UcdTN-oJnRpwZlFwA')
for i in response['items']:
    print(i['track']['artists'][0]['name'],i['track']['name'])

