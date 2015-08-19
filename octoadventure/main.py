from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from google.appengine.api import users
import sys

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class UserModel(ndb.Model):
    currentUser = ndb.StringProperty(required = True)
    
# gets information from user. We can modify this, I just wanted datastore to be set up. Also the required information doesn't act as required....where as the not required one does....how to fix?
class UserInfoModel(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    phone_number = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    dorm_building = ndb.StringProperty(required = True)
    dorm_room_number = ndb.IntegerProperty()

# class GroupModel(ndb.Model):
#     username= ndb.StringProperty(required=True)

class UserInfoHandler(webapp2.RequestHandler):
    def get(self):
        user_info_template = jinja_environment.get_template('templates/signup.html')
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
        user_room = int(self.request.get("room"))
        form = UserInfoModel(first_name = user_firstname, last_name = user_lastname, phone_number = user_phone, email = user_email, dorm_building = user_building, dorm_room_number = user_room)
        form.put()
        redirect_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(redirect_template.render())

# just a bunch of skeletal handlers. again, nothing set.
class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(home_template.render())

class CreateHandler(webapp2.RequestHandler):
    all = UserInfoModel(first_name="this is a user")
    def get(self):
        all_users=UserInfoModel.query().fetch()
        create_template = jinja_environment.get_template('templates/create.html')
        self.response.out.write(create_template.render({'users:all_users'}))

class ViewHandler(webapp2.RequestHandler):
    def get(self):
        view_template = jinja_environment.get_template('templates/view.html')
        self.response.out.write(view_template.render())

class ManageHandler(webapp2.RequestHandler):
    def get(self):
        manage_template = jinja_environment.get_template('templates/manage.html')
        self.response.out.write(manage_template.render())

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

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        profile_template = jinja_environment.get_template('templates/profile.html')
        self.response.out.write(profile_template.render())

app = webapp2.WSGIApplication([
    ('/', UserInfoHandler),
    ('/home', HomepageHandler),
    ('/create', CreateHandler),
    ('/view', ViewHandler),
    ('/manage', ManageHandler),
    ('/search', SearchHandler),
    ('/locate', LocateHandler),
    ('/maps', MapsHandler),
    ('/profile', ProfileHandler)
], debug=True)
