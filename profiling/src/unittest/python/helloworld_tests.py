from mockito import mock, verify
import unittest

from run import register,login,app


class FlaskTestCase(unittest.TestCase):
    
  #ensure that login works with correct credentials
  def test_correct_login(self):
    tester = app.test_client(self)
    response = tester.post(
      '/login',
      data = dict(username="test@gmail.com", password="test", login=""),
      follow_redirects=True
      )
    self.assertIn(b'Invalid Email and/or Password', response.data)
    