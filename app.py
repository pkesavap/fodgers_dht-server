from flask import Flask,render_template,request,session,logging,url_for,redirect,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt
from functools import wraps
import requests
import os

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.network_sqlite3'

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '1234567DHTCONSOLE'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    hosturl = db.Column(db.String(300), nullable=False)





@app.route("/registerNetwork", methods=["POST"])
def registerNetwork():
  
    db.create_all()
    #flash("File Uploaded", "success")
    print("praji")
    new_map= request.json
    print(new_map['email_field'])
    print(request.form.get("email_field"))
    if request.method == "POST":
        resp = jsonify(success=True)
        resp.status_code = 200
        email = new_map['email_field']
        hosturl = new_map["host_url_field"]
        new_map = Network(email=email, hosturl=hosturl)
        db.session.add(new_map)
        db.session.commit()
        return resp
 

    

@app.route("/")
def index():
    return "Hello World!"
