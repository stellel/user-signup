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
import re

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
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

class SignupForm(webapp2.RequestHandler):
	"""requests coming in to '/'"""
	def get(self):
		signup_header = "<h1>Signup Form</h1>"
		
		form_name = """
		<form action="/confirm" method="post">
		<label>
		    Name
		    <input type="text" name="username" />
		</label>"""

		#if we have an error make a <p> to display it
		error = self.request.get("error")
		error_element = "<p class='error'>" + error + "</p>" if error else ""
		
		form_password = """
		<p><label>
		    Password
		    <input type="text" name="password" />
		</label></p>
		<p>
		<label>Confirm Password
		    <input type="text" name="verify" />
		</label></p>
		"""
		
		form_email = """
		<p><label>
		    Email Address (optional)
		    <input type="text" name="email" />
		</label></p>
		"""
		
		form_submit = """
		<p><input type="submit" /></p>
		</form>
		"""

		


		main_content = signup_header + form_name + error_element + form_password + form_email + form_submit
		page_content = page_header + main_content + page_footer
		self.response.write(page_content)

class ConfirmSubmission(webapp2.RequestHandler):
	"""handles requests coming in to /confirm"""
	def post(self):
		username = self.request.get("username")

		if not username:
			# make a helpful error message
			error = "Please enter a user name."
			error_blank = cgi.escape(error, quote=True)
			# redirect to homepage, and include error as a query parameter in the URL
			self.redirect("/?error=" + error_blank)

		elif not valid_username(username):
			error_invalid_username = "That is not a valid user name."
			error = error_invalid_username
			self.redirect("/?error" + error)

		confirmation_message = "Welcome, " + username + "!"
		confirmation = page_header + "<p>" + confirmation_message + "</p>" + page_footer
		self.response.write(confirmation)



app = webapp2.WSGIApplication([
	('/', SignupForm),
	('/confirm', ConfirmSubmission)
], debug=True)
