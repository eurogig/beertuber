# Beertuber

This project is rather personal but others might find the code useful as a base for other projects.

It was designed to support reviews on my youtube channel called [BeerNative TV](https://www.youtube.com/channel/UCBu7uCQ93XoEdSS9JDVf2uA)

NOTE: The upload of youtube videos using authentication and the google ID of a project which hasn't been approved by Youtube specifically for uploading video will result in the video being private/locked.  To overcome this requirement you'll need to apply for API Client approval [here[(https://support.google.com/youtube/contact/yt_api_form)

The work flow assigned to this is as follows...

##Requirements: 
### Untappd
Environment variables that need to be set in advance are
UNTAPPD_CLIENT_ID
UNTAPPD_CLIENT_SECRET
UNTAPPD_USER

### Youtube
YT_CHANNEL_ID
YT_APIKEY
YT_PLAYLIST

### Set spreadsheet variable for beer logging. Search for line
```
wks = gc.open("BeerNativeDB")
```

1. Record a video of your beer experience in mp4 format.  (Ideally with OBS as it produces an mkv format which remuxes into a perfect mp4 for youtube.
2. Design a nice thumbnail for your video.
3. Manually upload your video to youtube and add it to a playlist.  Adding it to the playlist is required for the script to find the video URL and update it with the title and description. Put the playlist ID into the environment variable YT_PLAYLIST
4. Check the beer into Untappd as normal except at the end of your text description add a "- <beer scoring>".  The dash '-' is a delimiter.  See below for the beer scoring format.
eg. "Hard hitting hop forward with pine persistent throughout.  A nice long finish of stone fruit and bananas. - {"AC":5,"UN":4,"AR":5,"PA":3,"FL":9}"
5. Run the getlatestcheckin.py and it will begin and interactive session asking for hops, malts, yeasts and adjuncts.  It will pull your latest checkin from Untappd, parsing the scoring and the additional meta data provided by Untappd.  It will build the YouTube data (using jinja2 templates) for the title and description.  
6. It will add the title and description to your latest video in the playlist.
7. This will autopopulate a CSV google sheet which in my case populates the beer map at the [BeerNative TV website](https://beernative.tv)
8. *Not implemented yet but code present.* After the upload is complete it will download your available playlists and ask to which of these it should add this new video.  It does not yet create a new playlist.  

## Beer Scoring:
`{"AC":5,"UN":4,"AR":5,"PA":3,"FL":9}`
- AC = Accuracy (out of 5)
- UN = Uniqueness (out of 5)
- AR = Artwork for the can or bottle (out of 5)
- PA = Packaging quality or innovation (out of 5)
- FL = Flavour (out of 10)

This is a set of scripts designed to pull the latest checkin from your Untappd account (you'll need an API key from Untappd which is a royal pain to get), parse the output and use the jinja2 template to format it into a youtube video description.  

## Config files:

The scripts require the creation of two config files.  One for Untappd and another for Youtube in the format

### youtubeapiconfig.py
`youtubeapis = {
    "apikey": "your youtube api key",
    "apiversion": "v3",    
    "apiname": "youtube",
    "channelid": "your youtube channel id"
}`

### untappdconfig.py
`untappdcfg = {
    "client_id": "your Untappd client id",
    "client_secret": "your Untappd client secret",
    "username": "your Untappd username",
}`
> You can apply for the above Untappd credentials by creating an application at [Untappd](https://untappd.com/api)
