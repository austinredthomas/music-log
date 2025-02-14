import requests
import datetime
import sys

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
    tokenExpireTime = datetime.datetime.now() + datetime.timedelta(seconds = jsonResponse['expires_in'])
    return token, tokenExpireTime

def checkToken(tokenExpireTime):
    # Function for checking whether the current token is expired
    # Returns TRUE if valid, and FALSE if expired
    currentTime = datetime.datetime.now()
    if currentTime > tokenExpireTime:
        return False
    else:
        return True

def searchArtist(token):
    # get input from user
    q = input("Enter artist name: ")
    
    # set url, headers, and params for GET request
    url = "https://api.spotify.com/v1/search"
    headers = {
        'Authorization': 'Bearer  ' + token,
    }
    params = {
        'q': q,
        'type': 'artist'
    }
    
    # Make GET request and turn response into JSON
    response = requests.get(url, headers=headers, params=params)
    jsonResponse = response.json()
    print(jsonResponse['artists']['items'][0]['name'])
    
    # Iterate through artists and ask for confirmation
    for i in jsonResponse['artists']['items']:
        artistName = i['name']
        print("Is this your artist?: ", artistName)
        answer = input("(y/n)")
        if answer == "y" or answer == "Y":
            return i['id']

def getAlbum(artistID, token):
    print("Getting ArtistID: ", artistID, " albums...") 
    url = 'https://api.spotify.com/v1/artists/' + artistID + '/albums'
    headers = {
        'Authorization': 'Bearer  ' + token
    }
    params = {
        'include_groups': 'album'
    }
    response = requests.get(url, headers = headers, params = params)
    jsonResponse = response.json()
    for i in jsonResponse['items']:
        print("Album name: ", i['name'], "| Tracks: ", i['total_tracks'])

if __name__ == '__main__':
    def openMenu():
    # Open menu
        print("\nSelect option from menu:\n(1) Search for Artist's albums\n(2) Get tracklist of current listened to album\n(0) Exit")
        answer=int(input())
        if answer == 0:
            sys.exit()
        elif answer == 1:
            checkToken(tokenExpireTime)
            artistID = searchArtist(token)
            print("The artist you chose ID: ", artistID)
            getAlbum(artistID, token)
        elif answer == 2:
            print("we're about to get some info...")
        openMenu()

    # get Client ID and Client Secret
    f = open("clientID.txt", "r")
    lines = f.readlines()
    clientID = lines[0]
    f = open("clientSecret.txt", "r")
    lines = f.readlines()
    clientSecret = lines[0]
    # get token and store, track expiration time
    token, tokenExpireTime = requestToken(clientID, clientSecret)
    print(tokenExpireTime)
    if checkToken(tokenExpireTime) == False:
        print("Token is expired.")
    else:
        print("Token is valid.")
    print("Token: ", token)

    openMenu()
