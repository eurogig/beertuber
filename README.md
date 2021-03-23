# Beertuber

This project is rather personal but others might find the code useful as a base for other projects.

It was designed to support reviews on my youtube channel called [BeerNative TV](https://www.youtube.com/channel/UCBu7uCQ93XoEdSS9JDVf2uA)

The work flow assigned to this is as follows...

1. Record a video of your beer experience in mp4 format.  (Ideally with OBS as it produces an mkv format which remuxes into a perfect mp4 for youtube.
2. Design a nice thumbnail for your video and have that ready
3. Check the beer into Untappd as normal except at the end of your text description add a "- <beer scoring>".  The dash '-' is a delimiter.  See below for the beer scoring format.
eg. "Hard hitting hop forward with pine persistent throughout.  A nice long finish of stone fruit and bananas. - {"AC":5,"UN":4,"AR":5,"PA":3,"FL":9}"
4. Run the getlatestcheckin.py and it will begin and interactive session starting with pulling your latest checkin from Untappd, parsing the scoring and the additionally meta data provided by Untappd.  It will build the YouTube data (using jinja2 templates) required, ask for the location of the video and thumbnail (checking for size restrictions) and upload.  It by default sets the publish time for 2 hours in the future to allow for YouTube processing.  
5. After the upload is complete it will download your available playlists and ask which of these it should add this new video.  It does not yet create a new playlist.  That's for a future update.
6. (Not implemented yet) This will eventually autopopulate the database which populates the beer map at the [BeerNative TV website](https://beernative.tv)

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
