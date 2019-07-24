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
                email = user.nickname()
        )
            biscuit_user.put()
            self.redirect('/dogs')
            start_template = jinja_current_dir.get_template("survey.html")
            self.response.write(start_template.render())

class displayPage(webapp2.RequestHandler):
    def get(self):
        queryString = "type=dog&age=senior&breed=Akita&gender=female&size=large"
        api_url = "https://api.petfinder.com/v2/animals?" + queryString
        headers = {
            "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjliMGQyMzhhYmZmZDRjNWJhM2IyNjFjODFhMzI3Y2IzMzQyZDQwMGU2NDdmYzlkNjlkMzY4ZDI4NzZjMDQyMGZmMDdhY2U1OGQ4NjIxMWY5In0.eyJhdWQiOiJNZ2NVbHIxYm5NRmRGcDE4T2hxaEhhYVVhcmF4NDA4SUdLZVFOQ2VlV0czRmVDaUhWTSIsImp0aSI6IjliMGQyMzhhYmZmZDRjNWJhM2IyNjFjODFhMzI3Y2IzMzQyZDQwMGU2NDdmYzlkNjlkMzY4ZDI4NzZjMDQyMGZmMDdhY2U1OGQ4NjIxMWY5IiwiaWF0IjoxNTYzOTgyNTI0LCJuYmYiOjE1NjM5ODI1MjQsImV4cCI6MTU2Mzk4NjEyNCwic3ViIjoiIiwic2NvcGVzIjpbXX0.P5hEE3FF1D790AnTNv924i31_GxWHRSypojMrDe5lw47I2av5bAf6ksAmkBRAHHn-CL2zN6dA3kQCQx7GzhNq8En30g8pC3_iHjOrslr-hVgkv4SzpJCMadseIJ-UwKe_zvz7DwwMVzD_XyWeBwQ_2QtNWZaEMUjYjl6VD5Cv6_WxBm2FkwnhmXh0JBSW9inYhmb_jPMiEtRDqrAniC25FYBfk9k8kzznZrgdj0Y-5FoU2GVmhTSqovzlcH6x5P87RFiwak0Ba3at8e5r9hvZHloCE8e51j_2ZeuC6i70pfnTp0QNTjYCMezwfFla2Xdx1yZu4dfD_vou1B_-Gs2JQ"
                  }
        api_response = urlfetch.fetch(api_url, headers=headers).content
        api_response_json = json.loads(api_response)
        self.response.write(api_response_json["animals"])
        # print(api_response_json["animals"])
        #
        # print(api_response_json['animals'])
        # dog_matches = []
        # for dog_match in api_response_json['animals'][0:10]:
        #     dog_matches.append(dog_match["animals"])
        # matches = {
        #     "img": dog_matches
        # }

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
