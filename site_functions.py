from flask import session, redirect, url_for, render_template
import socket

class SiteFunctions():
    def valid_login(self, user, passwd):
        if user == "emiliano" and passwd == "conae":
            session["username"] = user
            return redirect(url_for('index'))        
        else:
            print("no coinciden usuario y clave")
            return render_template('login.html')
    
    def retrieve_unit_status(self,host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(b'0\n')
        data = s.recv(2048).decode()
        s.close()
        return data