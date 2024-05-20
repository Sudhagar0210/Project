# Project
YouTube API V3 Project

Table of Contents

1.Introduction
2.Features
3.Installation
4.Configuration
5.Usage
6.API Endpoints
7.Examples

Introduction:-

"This project is a Python application that interacts with YouTube API V3 to retrieve, search, and manage YouTube content. It provides an easy-to-use interface for accessing various YouTube services such as searching for videos, retrieving channel details, and managing playlists."

Features:-

* Search for channels,playlists and videos.
* Retrieve video details, comments, and statistics.
* Manage playlists: create, update, and delete.
* Fetch channel information and statistics.
* Authenticated requests for managing user-specific data.

Installation:-

Instructions on how to install the project.

Example:

1. Clone the repository

* git clone https://github.com/yourusername/youtube-api-v3-project.git

2. Install the required dependencies:

   * pip install google-api-python-client
   * pip install Streamlt
   * Pip Install oauth2client
   * pip install requests
   * pip install python-dotenv  

Configuration:-

Details on how to configure the project, especially regarding the YouTube API.

1. Obtain API Key from Google Developer Console:
   * Go to Google Developer Console.
   * Create a new project or select an existing project.
   * Enable the YouTube Data API v3.
   * Create credentials to obtain an API key.
2.Set up environment variables

   * export YOUTUBE_API_KEY='YOUR_API_KEY'

Usage:-

Instructions on how to use the project, including command-line options or examples.

Example
* python main.py --search "Python tutorials"


API Endpoints:-

List and describe the main API endpoints if your project exposes any.

* GET /channels: Fetches details of a specific channel.
* POST /playlists: Creates a new playlist.
* GET /videos: Retrieves a list of videos based on search criteria.

Examples:-

Below mentioned some example code to get the Channel details to print.

# Channel details API
import pprint
import googleapiclient.discovery
import googleapiclient.errors


api="AIzaSyBcaDqZlIc9jOnQ4uufyg_63AsQx92vwl0"
id="UCTQ5IpRQwMPmSoUqEADiozg"


api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"



# Get credentials and create an API client
youtube = googleapiclient.discovery.build(
api_service_name, api_version, developerKey= api)

channel_request = youtube.channels().list(
part="snippet,contentDetails,statistics",
id=id  
)

channel_response = channel_request.execute()
#pprint.pprint(channel_response)

channel_id=(channel_response['items'][0]['id'])
Playlist_Id=(channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
channel_name = (channel_response['items'][0]['snippet']['title'])
channel_type =(channel_response['items'][0]['kind'])
channel_description =(channel_response['items'][0]['snippet']['description'])
channel_views = (channel_response['items'][0]['statistics']['viewCount'])
#channel_published = (response['items'][0]['snippet']['publishedAt'])

print("Channel ID:", channel_id)
print("Playlist ID:", Playlist_Id)
print("Channel Name:", channel_name)
print("Channel Type:", channel_type)
print("Channel Description:", channel_description)
print("Channel Views:", channel_views)










