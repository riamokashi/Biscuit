import webapp2
from //api.petfinder.com/v2/types/{type}/breeds import

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
            logout_button = '<a href ="%s"> Log Out</a>' % logout_url

            existing_user = BiscuitUser.query().filter(BiscuitUser.email == email_address).get()
            if existing_user:
                pass
            else:
                top_line = self.request.get("top-line")
                bottom_line = self.request.get("bottom-line")
                meme_url = self.request.get("template")
                saved_dict = {
                    "name":
                    "breed":
                    "age":
                    "friendliness":
                }
            #put this in HTML file -->
                self.response.write('''You are a new user, please answer the survey questions
                    <form method= 'post' action='/'>
                    <input type='text' name='first_name'>
                    <input type='text' name='age'>
                    <input type='text' name='breed'>
                    <input type='text' name='friendliness'>
                    <input type='submit'>
                ''' % logout_button)
        else:
            login_url = users.create_login_url('/')
            login_button = '<a href ="%s"> Sign In</a>' % login_url
        self.response.write("Please Log in<br>" + loginbutton)
    def post(self):
        user = users.get_current_user()
        if user:
        biscuit_user = BiscuitUser(
            first_name=self.request.get('first_name'),
            age = int(self.request.get('age')),
            breed= self.request.get('breed'),
            friendliness= self.request.get('friendliness'),
            email = user.nickname()
        )
        biscuit_user.put()
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
