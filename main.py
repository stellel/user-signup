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
import webapp2
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup Form</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>

"""



# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

form = """
<form action="/confirm" method="post">
    <h1>Signup Form</h1>
    <br>
    <label>Name
        <input type="text" name="user-name">
    </label>
    <br>
    <label>Password
        <input type="text" name="password">
    </label>
    <br>
        <label>Confirm Password
        <input type="text" name="password">
    </label>
    <br>
    <label>Email Address (optional)
        <input type="text" name="email">
    </label>

    <br>
    <br>

    <input type="submit">
</form>
"""
class SignupForm(webapp2.RequestHandler):
    """requests coming in to '/'"""
    def get(self):

        form = """
        <form action="/confirm" method="post">
        <h1>Signup Form</h1>
        <br>
        <label>
            Name
            <input type="text" name="user-name">
        </label>
        <br>
        <label>
            Password
            <input type="text" name="password">
        </label>
        <br>
        <label>Confirm Password
            <input type="text" name="password">
        </label>
        <br>
        <label>
            Email Address (optional)
            <input type="text" name="email">
        </label>
        <br>
        <br>
            <input type="submit">
        </form>
        """

        page_content = form
        self.response.write(page_content)



class ConfirmSubmission(webapp2.RequestHandler):
	"""handles requests coming in to /confirm"""
	def post(self):
		user_name = self.request.get("user-name")
		confirmation_message = "Welcome, " + user_name + "!"
		confirmation = page_header + "<p>" + confirmation_message + "</p>" + page_footer
		self.response.write(confirmation)
		


app = webapp2.WSGIApplication([
    ('/', SignupForm),
    ('/confirm', ConfirmSubmission)
], debug=True)
