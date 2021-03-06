from google.appengine.ext import ndb
import webapp2
import jinja2
import os
import logging
from google.appengine.api import users
import sys

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class UserModel(ndb.Model):
    currentUser = ndb.StringProperty(required = True)

class GroupModel(ndb.Model):
    group = ndb.StringProperty(required = True)
    member1 = ndb.StringProperty(required = True)
    member2 = ndb.StringProperty(required = True)
    member3 = ndb.StringProperty(required = True)
    user_key = ndb.KeyProperty(UserModel)

class UserInfoModel(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    phone_number = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    dorm_building = ndb.StringProperty(required = True)
    dorm_room_number = ndb.IntegerProperty()

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
        form = UserInfoModel()
        user_firstname = self.request.get("firstname")
        user_lastname = self.request.get("lastname")
        user_phone = self.request.get("number")
        user_email = self.request.get("email")
        user_building = self.request.get("building")
        if self.request.get("room").isdigit():
            user_room = int(self.request.get("room"))
            form.dorm_room_number = user_room
        form.populate(first_name = user_firstname, last_name = user_lastname, phone_number = user_phone, email = user_email, dorm_building = user_building)
        form.put()
        redirect_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(redirect_template.render())
        # template_create = jinja_environment.get_template('templates/create.html')
        # self.response.out.write(template_create.render({'users': all_users}))
# just a bunch of skeletal handlers. again, nothing set.
class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_environment.get_template('templates/home.html')
        self.response.out.write(home_template.render())

class CreateHandler(webapp2.RequestHandler):
    def get(self):
        all_users = UserInfoModel.query().fetch()
        create_template = jinja_environment.get_template('templates/create.html')
        self.response.out.write(create_template.render({'users': all_users}))

    def post(self):
        group_name = self.request.get("groupname")
        group_member1 = self.request.get("groupmember1")
        group_member2 = self.request.get("groupmember2")
        group_member3 = self.request.get("groupmember3")

        logged_in_users = UserModel.query().fetch()
        current_user = users.get_current_user()
        # logging.info(logged_in_users[0])
        logging.info(current_user.user_id())
        for user in logged_in_users:
            logging.info(user.currentUser)
            if user.currentUser == current_user.user_id():
                current_user_key = user.key
                team = GroupModel(group = group_name, member1 = group_member1, member2 = group_member2, member3 = group_member3, user_key = current_user_key)
                team.put()
                break

        # user = UserModel(currentUser = current_user.user_id())
        # user.put()

        # user = users.get_current_user()
        # logging.info(user)
        # logging.info(user.user_id())
        # user = UserModel(currentUser = user.user_id())
        # user.group_key.append(team.key)
        # user.put()
        # user = users.get_current_user()
        # user.group_key.append(team.key)
        # user.put()

        group_template = jinja_environment.get_template('templates/create.html')
        self.response.out.write(group_template.render())

class ViewHandler(webapp2.RequestHandler):
    def get(self):
        # group_id =self.request.get("group_id")
        # group_key = ndb.Key(GroupModel, int(group_id))
        # group_list = group_key.get()
        all_groups = GroupModel.query().fetch()
        view_template = jinja_environment.get_template('templates/view.html')
        self.response.out.write(view_template.render({'groups': all_groups}))

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
        user_id = self.request.get("user_id")
        user_key = ndb.Key(UserInfoModel, int(user_id))
        user_profile = user_key.get()
        all_users = UserInfoModel.query().fetch()
        profile_template = jinja_environment.get_template('templates/profile.html')
        self.response.out.write(profile_template.render({'user': user_profile}))

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
