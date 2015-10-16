
import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


import unittest
from app.py import *

class TestApp(unittest.TestCase):

  def test_calc_times(self):
      self.assertEqual(calc_self("00:00", "2015-10-10", 1000), 'From Oct 11, 2015 09:05 to Oct 13, 2015 03:00')

if __name__ == '__main__':
    unittest.main()
