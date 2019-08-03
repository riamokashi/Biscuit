import webapp2
import jinja2
import os
import urllib
from google.appengine.api import urlfetch
import json
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime, timedelta


DOG_KEY = ndb.Key('dog_key','something')
API_TOKEN_URL = 'https://api.petfinder.com/v2/oauth2/token'

def get_or_remake_api_token():
    payload = urllib.urlencode({
    'grant_type': 'client_credentials',
    'contentType': 'application/x-www-form-urlencoded',
    'client_id': 'STzlFwjWT9V7OifJPLNE0W5sCMgeQfAS9WMMgmDHQ7rANPSmuO',
    'client_secret': 'gizrCSqTsn8qo2590HbklQ5yGDfOivPUgjwt3iN4',
    })
    api_response = urlfetch.fetch(API_TOKEN_URL, method=urlfetch.POST, payload=payload).content
    response_json = json.loads(api_response)
    api_token  = response_json['access_token']
    print("API token refreshed: %s" % api_token)
    return api_token

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

class firstPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/')
        else:
            login_url = users.create_login_url('/')
            login_button = '<a href="%s" class="signIn">Sign In</a>'  % login_url
            self.response.write(login_button)
            first_template = jinja_current_dir.get_template("firstPage.html")
            self.response.write(first_template.render())
class loginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            logout_url = users.create_logout_url('/')
            existing_user = BiscuitUser.query(ancestor=DOG_KEY).filter(BiscuitUser.email == email_address).get()
            if existing_user:
                self.redirect('/dogs')
            else:
                print("loginPage.get not registered")
                survey_template = jinja_current_dir.get_template("survey.html")
                self.response.write(survey_template.render())
        else:
            self.redirect('/firstpage')
    def post(self):
        user = users.get_current_user()
        if user:
            biscuit_user = BiscuitUser(
                parent = DOG_KEY,
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
            biscuit_user = BiscuitUser.query(ancestor=DOG_KEY).filter(BiscuitUser.email == user.nickname()).get()
            api_token = config["CONFIG_API_TOKEN_KEY"]
            headers = {
                "Authorization" : "Bearer {token}".format(token=api_token)
            }
            data_dict = {'photos': []}
            page_numbers = range(1,10)
            for page_number in page_numbers:
                queryString = "type=dog&age={age}&gender={gender}&size={size}&page={page_number}&limit=100&".format(age=biscuit_user.age, size=biscuit_user.size, gender=biscuit_user.gender, page_number=page_number)
                api_url = "https://api.petfinder.com/v2/animals?" + queryString
                api_response = urlfetch.fetch(api_url, headers=headers).content
                api_response_json = json.loads(api_response)
                for animal in api_response_json['animals']:
                    if(len(animal['photos']) > 0):
                        data_dict['photos'].append(animal['photos'][0]['large'])
            user = users.get_current_user()

            logout_url = users.create_logout_url('/')
            data_dict['logout_url']= logout_url

            display_template = jinja_current_dir.get_template("display.html")
            self.response.write(display_template.render(data_dict))

class aboutTheTeam(webapp2.RequestHandler):
    def get(self):
        about_template = jinja_current_dir.get_template("aboutus.html")
        self.response.write(about_template.render())

class Adopt(webapp2.RequestHandler):
    def get(self):
        adopt_template = jinja_current_dir.get_template("adopt.html")
        self.response.write(adopt_template.render())

config = {
    "CONFIG_API_TOKEN_KEY": get_or_remake_api_token(),
    "CONFIG_API_TOKEN_BIRTHDAY_KEY": datetime.now()
}

app = webapp2.WSGIApplication([
    ('/', loginPage ),
    ('/dogs', displayPage),
    ('/firstpage', firstPage),
    ('/aboutus', aboutTheTeam),
    ('/adopt', Adopt)
], debug=True)
