from __future__ import absolute_import

from flask import Flask, request, render_template, url_for,\
 session, flash,  redirect, escape, abort
from .aux import valid_login, retrieve_unit_status
from flask.helpers import make_response
import socket

__author__ = "Emiliano A. Baum"
__license__ = "GPLv3"
__description__ = "Indexing data module for ElasticSearch. Process "

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['USERNAME'] = 'soporte'
app.config['PASSWORD'] = 'cgss'

@app.route('/')
def index():
    return render_template('/index.html', title='Unit Status Viewer', )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('unit_status'))
    session['logged_in'] = None
    return render_template('login.html', title='Login', error=error)
            
@app.route('/logout')
def logout():
    session['username'] = ''
    session['logged_in'] = None
    flash('You were logged out')
    return redirect(url_for('index'),200)


@app.route('/unit_status',methods=['GET'])
def unit_status():
    try:
        telemetry = retrieve_unit_status()
        session['marktime'] = telemetry.split('|')[0] 
        session['unit'] = telemetry.split('|')[1]
        session['telemetry'] = (telemetry.split('|')[2]).split(';')
        print("telemetry: ",session['telemetry'])
    except Exception as e:
        print("Connection error: ",e)
        session['error'] = "%s"%e
        pass
    return render_template('unit_status.html', 
                           title='Unit Status Viewer', user=session['username']) 
        
