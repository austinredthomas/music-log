import requests

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
    q = input("Enter artist name: ")
    url = "https://api.spotify.com/v1/search"
    # Create header (Authorization, Content-Type)
    headers = {
        'Authorization': 'Bearer  ' + token,
    }
    params = {
        'q': q,
        'type': 'artist'
    }
    response = requests.get(url, headers=headers, params=params)
    jsonResponse = response.json()
    print(jsonResponse['artists']['items'][0]['name'])
    for i in jsonResponse['artists']['items']:
        artistName = i['name']
        print("Is this your artist?: ", artistName)
        answer = input("(y/n)")
        if answer == "y" or answer == "Y":
            return i['id']

def getAlbum(artistID, token):
    print("Getting ArtistID: ", artistID, " albums...") 
    url = 'https://api.spotify.com/v1/artists/' + artistID + '/albums'
    print(url)
    headers = {
        'Authorization': 'Bearer  ' + token
    }
    params = {
        'include_groups': 'album'
    }
    response = requests.get(url, headers = headers, params = params) # url, headers, params
    jsonResponse = response.json()
    print("Response: ", jsonResponse['items'][0])
    for i in jsonResponse['items']:
        print("Album name: ", i['name'], "| Tracks: ", i['total_tracks'])
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
    
    artistID = searchArtist(token)
    print("The artist you chose ID: ", artistID)
    
    getAlbum(artistID, token)
