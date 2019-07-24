import webapp2
import jinja2
import os
from google.appengine.api import urlfetch
import json
from google.appengine.api import users
from google.appengine.ext import ndb

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
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            logout_url = users.create_logout_url('/')
            existing_user = BiscuitUser.query().filter(BiscuitUser.email == email_address).get()
            if existing_user:
                self.response.write("Welcome back " + email_address)
                self.response.write("<br> <input type='button' name='template' value='log out'>")
                self.response.write("<a href='/dogs'>View your matches for today!</a>")
            else:
                survey_template = jinja_current_dir.get_template("survey.html")
                self.response.write(survey_template.render())
        else:
            login_url = users.create_login_url('/')
            login_button = '<a href ="%s"> Sign In</a>' % login_url
            self.response.write("Please Log in<br>" + login_button)
    def post(self):
        user = users.get_current_user()
        if user:
            biscuit_user = BiscuitUser(
                first_name=self.request.get('first_name'),
                age = self.request.get('age'),
                breed= self.request.get('breed'),
                size= self.request.get('size'),
                gender = self.request.get('Gender'),
                haveKids = self.request.get('kids'),
                email = user.nickname()
        )
            biscuit_user.put()
            self.redirect('/dogs')
            start_template = jinja_current_dir.get_template("survey.html")
            self.response.write(start_template.render())

class displayPage(webapp2.RequestHandler):
    def get(self):
        api_url = "https://api.petfinder.com/v2/animals"
        api_response = urlfetch.fetch(api_url).content
        api_response_json = json.loads(api_response)
            "animals": [
                {
                    "id": 120,
                    "organization_id": "NJ333",
                    "url": "https://www.petfinder.com/dog/spot-120/nj/jersey-city/nj333-petfinder-test-account/?referrer_id=d7e3700b-2e07-11e9-b3f3-0800275f82b1",
                    "type": "Dog",
                    "species": "Dog",
                    "breeds": {
                        "primary": "Akita",
                        "secondary": null,
                        "mixed": false,
                        "unknown": false
                    },
                    "colors": {
                        "primary": null,
                        "secondary": null,
                        "tertiary": null
                    },
                    "age": "Young",
                    "gender": "Male",
                    "size": "Medium",
                    "coat": null,
                    "attributes": {
                        "spayed_neutered": false,
                        "house_trained": true,
                        "declawed": null,
                        "special_needs": true,
                        "shots_current": false
                    },
                    "environment": {
                        "children": false,
                        "dogs": false,
                        "cats": false
                    },
                    "tags": [
                        "Cute",
                        "Intelligent",
                        "Large",
                        "Playful",
                        "Happy",
                        "Affectionate"
                    ],
                    "name": "Spot",
                    "description": "Spot is an amazing dog",
                    "photos": [
                        {
                            "small": "http://photos.petfinder.com/photos/pets/42706540/1/?bust=1546042081&width=100",
                            "medium": "http://photos.petfinder.com/photos/pets/42706540/1/?bust=1546042081&width=300",
                            "large": "http://photos.petfinder.com/photos/pets/42706540/1/?bust=1546042081&width=600",
                            "full": "http://photos.petfinder.com/photos/pets/42706540/1/?bust=1546042081"
                        }
                    ],
                    "status": "adoptable",
                    "published_at": "2018-12-22T20:31:32+0000",
                    "contact": {
                        "email": "petfindertechsupport@gmail.com",
                        "phone": "111-333-5555, 222-333-5555, 333-333-5353, 111-333-2222",
                        "address": {
                            "address1": "Test address 1",
                            "address2": "Test address 2",
                            "city": "Jersey City",
                            "state": "NJ",
                            "postcode": "07097",
                            "country": "US"
                        }
                    },
                    "_links": {
                        "self": {
                            "href": "/v2/animals/120"
                        },
                        "type": {
                            "href": "/v2/types/dog"
                        },
                        "organization": {
                            "href": "/v2/organizations/nj333"
                        }
                    }
                }
            ],
            "pagination": {
                "count_per_page": 20,
                "total_count": 1,
                "current_page": 1,
                "total_pages": 1,
                "_links": {
                    "previous": {
                        "href": "/v2/animals?type=dog&page=1"
                    },
                    "next": {
                        "href": "/v2/animals?type=dog&page=3"
                    }
                }
            }
        }
        display_template = jinja_current_dir.get_template("display.html")
        self.response.write(display_template.render())




app = webapp2.WSGIApplication([
    ('/', loginPage ),
    ('/dogs', displayPage)
], debug=True)

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
