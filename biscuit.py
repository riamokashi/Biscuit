import webapp2
from //api.petfinder.com/v2/types/{type}/breeds import

jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class loginPage(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/biscuit.html")
        self.response.write(start_template.render())
class questionPage
    def post():
        start_template = jinja_current_dir.get_template("templates/question.html")
        self.response.write(start_template.render())

app = webapp2.WSGIApplication([
    ('/login', loginPage ),
    ('/question', questionPage)
], debug=True)


        top_line = self.request.get("top-line")
        bottom_line = self.request.get("bottom-line")
        meme_url = self.request.get("template")
