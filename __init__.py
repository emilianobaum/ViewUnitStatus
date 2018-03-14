#!/usr/bin/python3
#-*-coding: utf-8  -*-
from __future__ import absolute_import
from load_config import ConfigData
from site_functions import SiteFunctions
from flask import Flask, request, render_template, url_for,\
 session, flash,  redirect, escape, abort
from flask.helpers import make_response
import logging
import logging.handlers

__author__ = "Emiliano A. Baum"
__license__ = "GPLv3"
__description__ = "Indexing data module for ElasticSearch. Process "

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# Loading modules
CD =ConfigData("configuration/configuration.json")
SF = SiteFunctions()
logger = logging.getLogger("Unit Status")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(filename=('%s/%s'%
                                                         (CD.dirLog, CD.fileLog)), mode='a', 
                                                         maxBytes=5000000, backupCount=5, 
                                                         encoding='utf-8')
formatter = logging.Formatter("%(asctime) 15s - %(process)d - %(name)s -\
                                                                        %(lineno)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route('/')
def index():
    return render_template('/index.html', title='Unit Status Viewer', )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
            logger.warning("%s: %s."%(request.form['username'], error))
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
            logger.warning("%s: %s."%(request.form['password'], error))
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            logger.info("User %s login"%session['username'])
            return redirect(url_for('unit_status'))
    session['logged_in'] = None
    return render_template('login.html', title='Login', error=error)
            
@app.route('/logout')
def logout():
    session['username'] = ''
    session['logged_in'] = None
    flash('%s is logged out'%session['username'])
    logger.info('%s is logged out'%session['username'])
    return redirect(url_for('index'),200)

@app.route('/unit_status',methods=['GET'])
def unit_status():
    try:
        telemetry = SF.retrieve_unit_status(CD.srvrHost, CD.srvrPort)
        session['marktime'] = telemetry.split('|')[0] 
        session['unit'] = telemetry.split('|')[1]
        session['telemetry'] = (telemetry.split('|')[2]).split(';')
        logger.info('Showing unit status')
    except Exception as e:
        session['error'] = "%s"%e
        logger.error(session['error'])
        pass
    return render_template('unit_status.html', 
                           title='Unit Status Viewer', user=session['username'])

if __name__ == "__main__":
    CD.load_file('configuration/configuration.json')

    app.run(host=CD.webHost, port=CD.webPort, debug=True)
    app.config['USERNAME'] = CD.userConf
    app.config['PASSWORD'] = CD.passwdConf
