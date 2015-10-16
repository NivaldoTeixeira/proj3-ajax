"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

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


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############

def calc_times(time, date, miles):
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  
  h = time[:time.find(':')]
  m = time[(time.find(':') + 1):]
  date = date.replace(hours=+int(h))
  date = date.replace(minutes=+int(m))

  if (miles == 0):
      opening_time = str(date.format('MMM DD, YYYY HH:mm'))
      closing_time = str(date.replace(hours=+1).format('MMM DD, YYYY HH:mm'))
  else:
      opening_time = str(date.replace(hours=+get_opening_time(miles)).format('MMM DD, YYYY HH:mm'))
      closing_time = str(date.replace(hours=+get_closing_time(miles)).format('MMM DD, YYYY HH:mm'))
      
  miles = "From " + opening_time + " to " + closing_time
  return miles

@app.route("/_calc_times")
def jsonify_calc_times():
    app.logger.debug("Got a JSON request");

    miles = request.args.get('miles', 0, type=int)
    metric = request.args.get('metric', 0, type=str)
    if (metric == "miles"):
        miles = round(miles * 1.60934)


    str_date = request.args.get('date', 0, type=str)
    date = arrow.get(str_date)  
    time = request.args.get('time', 0, type=str)

    return jsonify(result=calc_times(time, date, miles))


#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"

def get_opening_time(distance):
    cont = 0
    if (distance <= 200):
        cont = distance / 34
    elif (distance <= 400):
        cont = 200 / 34 + (distance - 200) / 32
    elif (distance <= 600):
        cont = 200 / 34 + 200 / 32 + (distance - 400) / 30
    elif (distance <= 1000):
        cont = 200 / 34 + 200 / 32 + 200 / 30 + (distance - 600) / 28
    elif (distance <= 1300):
        cont = 200 / 34 + 200 / 32 + 200 / 30 + 400 / 28 + (distance - 1000) / 26
    return cont

def get_closing_time(distance):
    cont = 0
    if (distance <= 200):
        cont = distance / 15
    elif (distance <= 400):
        cont = 200 / 15 + (distance - 200) / 15
    elif (distance <= 600):
        cont = 200 / 15 + 200 / 15 + (distance - 400) / 15
    elif (distance <= 1000):
        cont = 200 / 15 + 200 / 15 + 200 / 15 + (distance - 600) / 11.428
    elif (distance <= 1300):
        cont = 200 / 15 + 200 / 15 + 200 / 15 + 400 / 11.428 + (distance - 1000) / 13.333
    return cont

#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
