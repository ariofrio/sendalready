import jinja2
import webapp2
import os

from google.appengine.api import users
from google.appengine.api import mail

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class SendRoute(webapp2.RequestHandler):
  def post(self):
    to = self.request.get('to')
    subject = self.request.get('subject')
    body = self.request.get('body')

    if not to or not subject or not body or not mail.is_email_valid(to):
      return self.redirect('/?error=Please+fill+out+all+fields+and+use+a+valid+recipient+email+address.')

    mail.send_mail(users.get_current_user().email(), to, subject, body)
    self.redirect('/?success=Successfully+sent+your+email.')

class IndexRoute(webapp2.RequestHandler):
  def get(self):
    data = {
      'user': users.get_current_user(),
      'login_url': users.create_login_url(self.request.uri),
      'logout_url': users.create_logout_url(self.request.uri),
      'success': self.request.get('success'),
      'error': self.request.get('error'),
    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(data))

app = webapp2.WSGIApplication([
  ('/', IndexRoute),
  ('/send', SendRoute)
])
