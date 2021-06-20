import requests
import inquirer
import untappd_noauth
import untappdconfig as cfg
import youtubeapiconfig as YTcfg
from jinja2 import Template
import json
import datetime
from Google import Create_Service
from Google import create_youtube
from googleapiclient.http import MediaFileUpload
import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

# Get the beer types dictionary
beer_types = pd.read_csv('beertypes.csv', header=None, index_col=0, squeeze=True).to_dict()

# PART 1 : Get the latest checkin from UnTappd

# Create the Untappd connection
myUntappd=untappd_noauth.Untappd(cfg.untappdcfg["client_id"],cfg.untappdcfg["client_secret"],cfg.untappdcfg["username"])

# Get the details of the last check in to Untappd
review = myUntappd.get_latest_checkin()

class BeerReview:

    def __init__(self, review):
        self.checkin_comment = review["response"]['checkins']["items"][0]["checkin_comment"]
        self.checkin_date = review["response"]['checkins']["items"][0]["created_at"]
        self.rating_score = review["response"]['checkins']["items"][0]["rating_score"]
        self.beer_name = review["response"]['checkins']["items"][0]["beer"]["beer_name"]
        self.bid = review["response"]['checkins']["items"][0]["beer"]["bid"]
        self.beer_style = review["response"]['checkins']["items"][0]["beer"]["beer_style"]
        self.beer_abv = review["response"]['checkins']["items"][0]["beer"]["beer_abv"]       
        self.brewery_name = review["response"]['checkins']["items"][0]["brewery"]["brewery_name"]
        self.country_name = review["response"]['checkins']["items"][0]["brewery"]["country_name"]
        self.url = review["response"]['checkins']["items"][0]["brewery"]["contact"]["url"]
        self.twitter = review["response"]['checkins']["items"][0]["brewery"]["contact"]["twitter"]
        self.facebook = review["response"]['checkins']["items"][0]["brewery"]["contact"]["facebook"]
        self.brewery_city = review["response"]['checkins']["items"][0]["brewery"]["location"]["brewery_city"]
        self.lat = review["response"]['checkins']["items"][0]["brewery"]["location"]["lat"]
        self.lng = review["response"]['checkins']["items"][0]["brewery"]["location"]["lng"]
        self.brewery_state = review["response"]['checkins']["items"][0]["brewery"]["location"]["brewery_state"]
        if review["response"]['checkins']["items"][0]["media"]["count"] > 0:
            self.photo_img_og = review["response"]['checkins']["items"][0]["media"]["items"][0]["photo"]["photo_img_og"]

        # Get the extra details of the beer as the checkin only had partial details
        beer = myUntappd.get_beer_detail(self.bid)
        #print("\n\n BEER")
        #
        # 
        # 
        # print(beer)
        self.beer_ibu = beer["response"]["beer"]["beer_ibu"] 
        self.beer_description = beer["response"]["beer"]["beer_description"]
        self.rating_count = beer["response"]["beer"]["rating_count"]
        self.overall_score = beer["response"]["beer"]["rating_score"]

    def set_scores(self, scores):
        # 
        self.accuracy = scores["AC"]
        self.flavour = scores["FL"]
        self.artwork = scores["AR"]
        self.uniqueness = scores["UN"]
        self.packaging = scores["PA"]
        self.total_score = scores["PA"] + scores["UN"] + scores["AR"] + scores["FL"] + scores["AC"]

    def set_hops(self, hops):
        # 
        self.beer_hops = hops      

    def set_malts(self, malts):
        # 
        self.beer_malts = malts          

    def set_yeast(self, yeast):
        # 
        self.beer_yeast = yeast      

    def set_adjuncts(self, adjuncts):
        # 
        self.beer_adjuncts = adjuncts   



def add_video_to_playlist(youtube,videoID,playlistID):
    add_video_request=youtube.playlistItems().insert(
    part="snippet",
    body={
        'snippet': {
            'playlistId': playlistID, 
            'resourceId': {
                    'kind': 'youtube#video',
                'videoId': videoID
            }
        #'position': 0
        }
    }
    ).execute()



print ("RAW REVIEW")
print (review)


beerreview = BeerReview(review)

print("Got:\n")
print(beerreview.beer_name)
print(beerreview.beer_description)

#read string from user
beer_hops=input("Enter Hops (comma separated e.g. citra, vic secret): ")
beerreview.set_hops(beer_hops)

beer_malts=input("Enter Malts (comma separated e.g. Golden Naked Oats, Golden Promise, Wheat): ")
beerreview.set_malts(beer_malts)

beer_yeast=input("Enter Yeast (comma separated e.g. WLP001 California Ale): ")
beerreview.set_yeast(beer_yeast)

beer_adjuncts=input("Enter Adjuncts (comma separated e.g. cacao, snake oil): ")
beerreview.set_adjuncts(beer_adjuncts)

# Grab the encoded review scores from the Untappd review eg 
# {"AC":4,"UN":3,"AR":5,"PA":3,FL:8}
# Where AC = Accurcy, UN = Uniqueness, AR = Artwork, PA = Packaging, FL = Flavour
# In the Untappd review the format is "blah blah blah I like it -[encoded score]"

desc = beerreview.checkin_comment.split("-")

if len(desc) > 1:
# Replace all weird forms of single quote just in case I was lazy and didn't use double quotes
    desc[1] = str(desc[1]).replace("’", "\"")
    desc[1] = str(desc[1]).replace("‘", "\"")
    desc[1] = str(desc[1]).replace("'", "\"")
    desc[1] = str(desc[1]).replace('”', "\"")
    desc[1] = str(desc[1]).replace('“', "\"")
    desc[1] = str(desc[1]).replace('[', '{')
    desc[1] = str(desc[1]).replace(']', '}')
    #desc[1] = str(desc[1]).replace('3.5', 'PA:3') 

    print(desc[1])
    beer_scores = json.loads(desc[1])

    print("Scores:")
    print(beer_scores)

    beerreview.set_scores(beer_scores)

with open ("youtubetemplate.txt", "r") as myfile:
    youtubetemplate=myfile.read()

print (youtubetemplate)

tm = Template(youtubetemplate)
video_description = tm.render(b=beerreview)

print(video_description)

###############################################################
# PART 2 : Get the latest video ID 
###############################################################

CLIENT_SECRET_FILE = 'my_client_secrets.json'
API_NAME = YTcfg.youtubeapis["apiname"]
API_VERSION = YTcfg.youtubeapis["apiversion"]
API_KEY = YTcfg.youtubeapis["apikey"]
SCOPES = ['https://www.googleapis.com/auth/youtube','https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube.readonly']
#SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
PUBLISH_OFFSET = 3 # Hours from now until the video is published to allow for processing
CATEGORY = 24 # Entertainment
DEFAULT_TAGS = ['beer' ,'craft beer','beer review','craft beer review','session ale','beernative','beer native','steve giguere','hazy ipa review',beerreview.brewery_name,beerreview.beer_name,beerreview.beer_style]
TITLE_TEMPLATE = "{{ b.beer_name }} by {{ b.brewery_name }} | {{ b.beer_style }}  | Beer Review"

# Create the youtube connection.  This might ask you to authenticate using the browser the first time
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

video_request = service.playlistItems().list(
        part="snippet",
        maxResults=1,
        playlistId="PL2zDI8OYY18rGVGAE4hHvfMJIOGfA5oaJ"
    )
video_response = video_request.execute()

video_id  = str(video_response["items"][0]["snippet"]["resourceId"]["videoId"])
video_url  = "https://youtu.be/" + video_id
print(video_url)


###############################################################
# PART 3 : Push it up the spreadsheet that updates the map 
###############################################################
CLIENT_SECRET_FILE = 'nice-symbol-285214-26e047279db0.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://spreadsheets.google.com/feeds'
]

# authorise against our gcloud account
credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, SCOPES)

gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
wks = gc.open("BeerNativeDB")
#wks = gc.open_by_key("1ifc13yVs8EATsBEkakQ52_7y4K4OS8w2yYJAZvO5rvc")

row = [
    beerreview.checkin_date,
    1, #map id hardcoded
    beerreview.brewery_name + ',' + beerreview.brewery_city + ',' + beerreview.brewery_state + ',' + beerreview.country_name,
    video_description,
    beerreview.photo_img_og,
    video_url,
    beerreview.lat,
    beerreview.lng,
    '',
    2, #hardcoded vakue for map
    beerreview.beer_name,
    '',
    beer_types[beerreview.beer_style],
    1,
    '',
    '',
    '',
    beerreview.beer_style,
    beerreview.beer_hops,
    beerreview.beer_malts,
    beerreview.beer_yeast,
    beerreview.beer_adjuncts,
    beerreview.beer_abv,
    beerreview.beer_ibu,
    beerreview.accuracy,
    beerreview.uniqueness,
    beerreview.artwork,
    beerreview.packaging,
    beerreview.flavour,
    beerreview.total_score,
    beerreview.rating_score,
    beerreview.overall_score
]
wks.sheet1.append_row(row)


###############################################################
# PART 4 : Push the title & description and meta data up to YouTube with an optional thumbnail 
###############################################################


# Set the publish time to be now + and offset (above) to allow for slow youtube processing
# The publish date is not used yet in the script
publish = (datetime.datetime.today() + datetime.timedelta(hours=PUBLISH_OFFSET)).isoformat("T","seconds")  + '.000Z'

titletm = Template(TITLE_TEMPLATE)
video_title = titletm.render(b=beerreview)

print(video_title)
print("Publishing set to:")
print(publish)

# Create the upload request
# Need to add video language and recording date and location
# Also add title and brewery to the tags 
request_body = {
    "id" : video_id,
    'snippet': {
        'categoryId': CATEGORY,
        'title': video_title,
        'description': video_description,
        'tags': DEFAULT_TAGS
    }
}


#MAX_THUMB_SIZE = 1925246
#while True:
#  try:
#    thumbnail_file = input('Enter path to thumbnail: ')
#    exists = os.path.isfile(thumbnail_file)
#    size = (os.stat('thumbnail.jpg').st_size < MAX_THUMB_SIZE)
#    if exists:
#      print ("Got thumb!")
#      break
#    else:
#      print ("thumbnail doesn't exists or is too big... try again")  
#  except ValueError:
#    print("Invalid")
#    continue#

print (request_body)

response_upload = service.videos().update(
#    part='snippet,status',
    part='snippet',
    body=request_body
).execute()

print(response_upload)

#service.thumbnails().set(
#    videoId=response_upload.get('id'),
#    media_body=MediaFileUpload(thumbnail_file)
#).execute()

exit()

# Eventually add the platlist chooser
service = create_youtube(API_NAME, API_VERSION, API_KEY)

print("Getting playlists...")
playlists = service.playlists().list (
    part="contentDetails, snippet",
    channelId=YTcfg.youtubeapis["channelid"],
    maxResults=50
).execute()

pl=[]
plIds={}
for item in playlists["items"]:
    print (item["snippet"]["title"],item["id"] )
    pl.append(item["snippet"]["title"])
    plIds[item["snippet"]["title"]]=item["id"]
#print(playlists)


questions = [
  inquirer.Checkbox('playlists',
                    message="Which playlists shall we add the video to?",
                    choices=pl,
                    ),
]
answers = inquirer.prompt(questions)
print(answers)

for pls in answers["playlists"]:
    print()
    print("Adding to playlist:")
    print (plIds[pls])
    result = add_video_to_playlist(service,str(response_upload.get('id')),plIds[pls])
    print (result)



