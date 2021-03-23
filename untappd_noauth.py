import requests

# Define a variable
Module = "Untappd NoAuth Get"

# Untappd v4 API base url
untappd_api_v4="https://api.untappd.com/v4"

# User based public routes
checkins="/user/checkins/"
beers="/user/beers/"
userinfo="/user/info/"
thepub = "/thepub/local"

# Define a class of untappd for a specific person
class Untappd:
    def __init__(self, client_id, client_secret, user_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.rate_limit = 100
        self.rate_remaining = 100
        self.user_id = user_id + "/"
        self.api_auth="?client_id=" + client_id + "&client_secret=" + client_secret

    def get_latest_checkin(self):
        return self.get_checkins(1)

    def get_checkins(self, limit=25):
        api_url=untappd_api_v4 + checkins + self.user_id + self.api_auth + "&limit=" + str(limit) 
        return self.get_api_json(api_url)
        
    def get_latest_beer(self):
        return self.get_beers(1)

    def get_beers(self, limit=25):
        api_url=untappd_api_v4 + beers + self.user_id + self.api_auth + "&limit=" + str(limit) 
        return self.get_api_json(api_url)

    def get_user_info(self):
        api_url=untappd_api_v4 + userinfo + self.user_id + self.api_auth 
        return self.get_api_json(api_url)

    def get_api_json(self,url):
        req = requests.get(url)
        self.rate_limit = req.headers['X-Ratelimit-Limit']
        self.rate_remaining = req.headers['X-Ratelimit-Remaining']
        req_json = req.json()
        return req_json   

    def get_rate_limit(self):  
        return self.rate_limit

    def get_rate_limit_remaining(self):  
        return self.rate_remaining        

#996973141 996896449 or 811128591

    def get_pubs_by_checkin(self, lat, lng, limit=25, radius=10, units="m"):
        api_url=untappd_api_v4 + thepub + self.api_auth + \
            "&limit=" + str(limit) + \
            "&lat=" + str(lat)  + \
            "&lng=" + str(lng)  + \
            "&radius=" + str(radius) + \
            "&max_id=996973141" + \
            "&dist_pref=" + str(units) 
        print(api_url)
        return self.get_api_json(api_url)          