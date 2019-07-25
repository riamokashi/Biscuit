import webapp2
import jinja2
import os
import urllib
from google.appengine.api import urlfetch
import json
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime, timedelta

CONFIG_API_TOKEN_KEY = 'api_key'
CONFIG_API_TOKEN_BIRTHDAY_KEY = 'api_key_birthdate'
API_TOKEN_URL = 'https://api.petfinder.com/v2/oauth2/token'
TOKEN_EXPIRATION_MILLIS = 55*60*1000  # 55 minutes * 60 seconds * 1000 milliseconds

def refresh_api_token():
    payload = urllib.urlencode({
    'grant_type': 'client_credentials',
    'contentType': 'application/x-www-form-urlencoded',
    'client_id': 'MgcUlr1bnMFdFp18OhqhHaaUarax408IGKeQNCeeWG3FeCiHVM',
    'client_secret': 'wu9uGytjSbQsPUj3uv6vNvj1gwolHDqvgyQoQjkU',
    })
    api_response = urlfetch.fetch(API_TOKEN_URL, method=urlfetch.POST, payload=payload).content
    response_json = json.loads(api_response)
    api_token  = response_json['access_token']
    print("API token refreshed: %s" % api_token)
    return api_token

def get_api_token(requestHandler):
    token_birthdate = requestHandler.app.config.get(CONFIG_API_TOKEN_BIRTHDAY_KEY)
    if token_birthdate < datetime.now() - timedelta(milliseconds=TOKEN_EXPIRATION_MILLIS):
        token = refresh_api_token()
        requestHandler.app.config.update({CONFIG_API_TOKEN_KEY: token})
        requestHandler.app.config.update({CONFIG_API_TOKEN_BIRTHDAY_KEY: datetime.now()})
    return requestHandler.app.config.get(CONFIG_API_TOKEN_KEY)

class BiscuitUser(ndb.Model):
    first_name = ndb.StringProperty()
    age = ndb.StringProperty()
    breed = ndb.StringProperty()
    size = ndb.StringProperty()
    gender = ndb.StringProperty()
    haveKids = ndb.StringProperty()
    email = ndb.StringProperty()

jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class loginPage(webapp2.RequestHandler):
    def get(self):
        print("loginPage.get")
        user = users.get_current_user()
        if user:
            print("loginPage.get user exists")
            email_address = user.nickname()
            logout_url = users.create_logout_url('/')
            existing_user = BiscuitUser.query().filter(BiscuitUser.email == email_address).get()
            if existing_user:
                print("loginPage.get is registered")
                self.response.write("Welcome back " + email_address)
                self.response.write("<br> <input type='button' name='template' value='log out'>")
                self.response.write("<a href='/dogs'>View your matches for today!</a>")
            else:
                print("loginPage.get not registered")
                survey_template = jinja_current_dir.get_template("survey.html")
                self.response.write(survey_template.render())
        else:
            print("loginPage.get user doesn't exist")
            login_url = users.create_login_url('/')
            login_button = '<a href ="%s"> Sign In</a>' % login_url
            self.response.write("Please Log in<br>" + login_button)
    def post(self):
        print("loginPage.post")
        user = users.get_current_user()
        if user:
            print("loginPage.post creating biscuituser")
            biscuit_user = BiscuitUser(
                first_name=self.request.get('first_name'),
                age = self.request.get('Age'),
                breed= self.request.get('Breed'),
                size= self.request.get('Size'),
                gender = self.request.get('Gender'),
                email = user.nickname()
            )
            biscuit_user.put()
            self.redirect('/dogs')



class displayPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            print("USER NICKNAME! " + user.nickname())
            biscuit_user = BiscuitUser.query().filter(BiscuitUser.email == user.nickname()).get()
            print("BISCUIT USER: "+ str(biscuit_user))
            queryString = "type=dog&breed={breed}&gender={gender}&size={size}".format(age=biscuit_user.age, breed=biscuit_user.breed, size=biscuit_user.size, gender=biscuit_user.gender)
            api_url = "https://api.petfinder.com/v2/animals?" + queryString
            print('api_url: ' + api_url)
            # print("API TOKEN: " + API_TOKEN)
            headers = {
                "Authorization" : "Bearer {token}".format(token=get_api_token(self))
                      }
            api_response = urlfetch.fetch(api_url, headers=headers).content
            api_response_json = json.loads(api_response)

            # print("API RESPONSE JSON: " + str(api_response_json))
            data_dict = {'photos': []}
            for animal in api_response_json['animals']:
                for photo in animal['photos']:
                    data_dict['photos'].append(photo['large'])
                    break
            logout_url = users.create_logout_url('/')
            logout_button = '<a href="%s"> Logout </a>' % logout_url


            display_template = jinja_current_dir.get_template("display.html")
            self.response.write(display_template.render(data_dict))
        # print(api_response_json["animals"])
        #
        # print(api_response_json['animals'])
        # dog_matches = []
        # for dog_match in api_response_json['animals'][0:10]:
        #     dog_matches.append(dog_match["animals"])
        # matches = {
        #     "img": dog_matches
        # }
        #



config = {
    CONFIG_API_TOKEN_KEY: refresh_api_token(),
    CONFIG_API_TOKEN_BIRTHDAY_KEY: datetime.now()
}
app = webapp2.WSGIApplication([
    ('/', loginPage ),
    ('/dogs', displayPage)
], debug=True, config=config)

#meme generator for reference
# import webapp2
# import jinja2
# import os
# import time
# from models import memeInfo
# from google.appengine.ext import ndb
# from google.appengine.api import urlfetch
# import json
#
#
#
# # This initializes the jinja2 environment
# # THIS WILL BE THE SAME FOR EVERY APP YOU BUILD
# # Jinja 2.Environment is a CONSTRUCTOR
# jinja_env = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions = ['jinja2.ext.autoescape'],
#     autoescape = True)
#
# # meme_templates = ["https://i.imgflip.com/2/30b1gx.jpg",
# # "https://i.imgflip.com/2/21tqf4.jpg", "https://i.imgflip.com/2/320xfw.jpg", "https://i.imgflip.com/2/1o00in.jpg"]
#
# # curl -d 'template_id=112126428&username=danielkelleycssi&password=cssirocks&text0=thisisthetop&text1=thisisthebottom' https://api.imgflip.com/caption_image
#
# danielkelleycssi
# cssirocks
#
#
# # "/Users/cssi-labs/python/labs/appengine"
#
# # The handler section
# class MainPage(webapp2.RequestHandler):
#     def get(self):
#
#         api_url = "https://api.imgflip.com/get_memes"
#         imgflip_response = urlfetch.fetch(api_url).content
#         imgflip_response_json = json.loads(imgflip_response)
#         print(imgflip_response_json['data']['memes'])
#         meme_templates = []
#         for meme_template in imgflip_response_json['data']['memes'][0:10]:
#             meme_templates.append(meme_template["url"])
#         meme_dict = {
#             "imgs": meme_templates
#         }
#         welcome_template = jinja_env.get_template('welcome.html')
#         self.response.write(welcome_template.render(meme_dict))
#
#
#
# class resultPage(webapp2.RequestHandler):
#     def post(self):
#
#         image_api = https://api.imgflip.com/caption_image
#
#
#         top_line = self.request.get("top-line")
#         bottom_line = self.request.get("bottom-line")
#         meme_url = self.request.get("template")
#         data_dict = {
#             "top": top_line,
#             "bottom": bottom_line,
#             "url": meme_url
#         }
#
#         memeStore = memeInfo(memeLineTop = top_line, memeImage = meme_url, memeLineBot = bottom_line)
#
#         memeStore.put()
#
#
#         result_template = jinja_env.get_template('result.html')
#         self.response.write(result_template.render(data_dict))
#
#
#
#
#
#
#
# class allmemes(webapp2.RequestHandler):
#     def get(self):
#
#
#         allMemesPlace = {
#         "memeList": memeInfo.query().fetch()
#         }
#
#
#         all_memes_template = jinja_env.get_template('allmemes.html')
#
#         self.response.write(all_memes_template.render(allMemesPlace))
# # The app configuration section
# app = webapp2.WSGIApplication(
#     [
#         ('/', MainPage),
#         ('/result', resultPage),
#         ('/all', allmemes)
#     ],
#     debug = True
