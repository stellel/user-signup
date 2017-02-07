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

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return not email or email.strip() == "" or EMAIL_RE.match(email)


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
		error = cgi.escape(self.request.get("error"))
		error_element = "<p class='error'>" + error + "</p>" if error else ""
		
		form_password = """
		<p><label>
		    Password
		    <input type="text" name="password" />
		</label></p>
		"""
		no_password_error = cgi.escape(self.request.get("no_password_error"))
		no_password_error_element = "<p class='error'>" + no_password_error + "</p>" if no_password_error else ""

		form_password_confirm = """
		<p>
		<label>Confirm Password
		    <input type="text" name="verify" />
		</label></p>
		"""
		password_error = cgi.escape(self.request.get("password_error"))
		password_error_element = "<p class='error'>" + password_error + "</p>" if password_error else ""
		
		form_email = """
		<p><label>
		    Email Address (optional)
		    <input type="text" name="email" />
		</label></p>
		"""
		email_error = "<p class='error'>" + cgi.escape(self.request.get("email_error")) + "</p>" if error else ""
		
		form_submit = """
		<p><input type="submit" /></p>
		</form>
		"""

		main_content = signup_header + form_name + error_element + form_password + no_password_error_element + form_password_confirm + password_error_element + form_email + email_error + form_submit
		page_content = page_header + main_content + page_footer
		self.response.write(page_content)

class ConfirmSubmission(webapp2.RequestHandler):
	"""handles requests coming in to /confirm"""
	def post(self):
		hasError = False
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email =  self.request.get("email")
		url = "/?"

			# redirect to homepage, and include error as a query parameter in the URL
			

		if not username or not valid_username(username):
			error = "That is not a valid user name."
			hasError = True
			url += "error=That is not a valid user name&" 

		else:
			url += ""

		if not password:
			no_password_error = "Please enter a password."
			hasError = True
			url += "no_password_error=Please enter a password&"
		
		else:
			url += ""

		if password != verify:
			password_error = "The passwords don't match."
			hasError = True
			url += "password_error=The passwords don't match&"
		
		else:
			url += ""

		if not valid_email(email):
			email_error = "That is not a valid email address."
			hasError = True
			url += "email_error=That is not a valid email address&"

		else: 
			url += ""


		if hasError:	
			self.redirect(url)

		confirmation_message = "Welcome, " + username + "!"
		confirmation = page_header + "<p>" + confirmation_message + "</p>" + page_footer
		self.response.write(confirmation)


app = webapp2.WSGIApplication([
	('/', SignupForm),
	('/confirm', ConfirmSubmission)
], debug=True)
