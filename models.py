from google.appengine.ext import ndb

class BiscuitUser(ndb.Model):
    first_name = ndb.StringProperty()
    age = ndb.IntegerProperty()
    breed = ndb.StringProperty()
    good_with = ndb.StringProperty()
    email = ndb.StringProperty()
