from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from google.appengine.api import users
import sys

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class UserModel(ndb.Model):
    currentUser = ndb.StringProperty(required = True)

class UserInfoModel(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    phone_number = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    dorm_building = ndb.StringProperty(required = True)
    # dorm_room_number = ndb.IntegerProperty()

class UserInfoHandler(webapp2.RequestHandler):
    def get(self):
        user_info_template = jinja_environment.get_template('templates/user.html')
        self.response.out.write(user_info_template.render())

        user = users.get_current_user()

        if user:
            self.response.write('<br><br>' + "Welcome, ")
            self.response.write(str(user) + '<br><br><br>')
            user = UserModel(currentUser = user.user_id())
            user.put()
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user_firstname = self.request.get("firstname")
        user_lastname = self.request.get("lastname")
        user_phone = self.request.get("number")
        user_email = self.request.get("email")
        user_building = self.request.get("building")
        # user_room = int(self.request.get("room"))
        form = UserInfoModel(first_name = user_firstname, last_name = user_lastname, phone_number = user_phone, email = user_email, dorm_building = user_building)
        form.put()
        redirect_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(redirect_template.render())

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(home_template.render())

class CreateHandler(webapp2.RequestHandler):
    def get(self):
        create_template = jinja_environment.get_template('templates/create.html')
        self.response.out.write(create_template.render())

class ViewHandler(webapp2.RequestHandler):
    def get(self):
        view_template = jinja_environment.get_template('templates/view.html')
        self.response.out.write(view_template.render())

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        search_template = jinja_environment.get_template('templates/search.html')
        self.response.out.write(search_template.render())

class LocateHandler(webapp2.RequestHandler):
    def get(self):
        locate_template = jinja_environment.get_template('templates/locate.html')
        self.response.out.write(locate_template.render())

class MapsHandler(webapp2.RequestHandler):
    def get(self):
        maps_template = jinja_environment.get_template('templates/maps.html')
        self.response.out.write(maps_template.render())

app = webapp2.WSGIApplication([
    ('/', UserInfoHandler),
    ('/home', HomepageHandler),
    ('/create', CreateHandler),
    ('/view', ViewHandler),
    ('/search', SearchHandler),
    ('/locate', LocateHandler),
    ('/maps', MapsHandler)
], debug=True)
