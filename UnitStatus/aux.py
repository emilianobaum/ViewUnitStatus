from flask import session, redirect, url_for, render_template
import socket

def valid_login(user, passwd):
    print("User: ",user)
    print("Type User",type(user))
    print("Passwd: ",passwd)
    print("Type Passwd",type(passwd))
    if user == "emiliano" and passwd == "conae":
        session["username"] = user
        return redirect(url_for('index'))        
    else:
        print("no coinciden usuario y clave")
        return render_template('login.html')

def retrieve_unit_status():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 10405))
    s.send(b'0\n')
    data = s.recv(1024).decode()
    print("DATA: ",data)
    s.close()
    return data