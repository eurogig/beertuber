import requests
import untappd_noauth
import untappdconfig as cfg
import json

# Get the untappd service object to call the SDK
myUntappd=untappd_noauth.Untappd(cfg.untappdcfg["client_id"],cfg.untappdcfg["client_secret"],cfg.untappdcfg["username"])

# Get the details of the last check in to Untappd
#checkindetail = requests.get('https://api.untappd.com/v4/user/checkins/stevegiguere?limit=1&client_id=009208CDB5C1D2E7AD3C8F139FA5B94F2EE4DFEA&client_secret=1910A4B6A6BE4382FA5BA0EAFFBD90D194EB7F28')
review = myUntappd.get_pubs_by_checkin(52.9098368,-0.640, 5 , 25)

print(json.dumps(review))