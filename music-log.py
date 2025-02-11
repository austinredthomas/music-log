import requests
import json

# Get valid access token from Spotify API
def requestToken(clientID, clientSecret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    data = {
        'grant_type':'client_credentials',
        'client_id': clientID,
        'client_secret': clientSecret
    }
    response = requests.post(url, data=data, headers=headers)
    jsonResponse = response.json()
    token = jsonResponse["access_token"]
    return token

def searchArtist(token):
    url = "https://api.spotify.com/v1/search"
    # Create header (Authorization, Content-Type)
    headers = {
        'Authorization': 'Bearer  ' + token,
    }
    params = {
        'q': 'muse',
        'type': 'artist'
    }
    response = requests.get(url, headers=headers, params=params)
    jsonResponse = response.json()
    print(jsonResponse['artists']['items'])
    for jsonResponse['artists']['items']:


def getAlbum():
    print("Getting album...")

if __name__ == '__main__':
    # get Client ID
    f = open("clientID.txt", "r")
    lines = f.readlines()
    clientID = lines[0]

    # get Client Secret
    f = open("clientSecret.txt", "r")
    lines = f.readlines()
    clientSecret = lines[0]

    # get token and store (only valid for 1 hour)
    token = requestToken(clientID, clientSecret)
    
    print("Token: ", token)
    
    searchArtist(token)
    
    getAlbum()
