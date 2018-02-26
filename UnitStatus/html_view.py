#!/usr/bin/python3
#-*- coding utf-8 -*-
import os
import socket
from flask import request, redirect, session, url_for, request, flash, render_template


class HTMLView():
    
    def index(self):
        return 'Hello world'

    def login(self):
        return True
    
    def logout(self):
        session.pop('logged_in', None)
        flash('You were logged out')
        return redirect(url_for('show_entries'))
    