#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
    dorm_room_number = ndb.IntegerProperty()

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
        user_room = int(self.request.get("room"))
        form = UserInfoModel(first_name = user_firstname, last_name = user_lastname, phone_number = user_phone, email = user_email, dorm_building = user_building, dorm_room_number = user_room)
        form.put()
        redirect_template = jinja_environment.get_template('templates/user.html')
        self.response.out.write(redirect_template.render())

# class HomepageHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', UserInfoHandler)
], debug=True)
