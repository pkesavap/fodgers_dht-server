from flask import Flask,render_template,request,session,logging,url_for,redirect,flash,jsonify,abort
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50),  nullable=False)
    hosturl = db.Column(db.String(300), nullable=False)

@app.route("/registerNetwork", methods=["POST"])
def registerNetwork():
    db.init_app(app)
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
        email_db = Network.query.filter_by(email=email).first()
        if email_db is not None:
            abort(404, f'email {email} already registered, please update the db')

        new_map = Network(email=email, hosturl=hosturl)
        db.session.add(new_map)
        db.session.commit()
        return resp
 
@app.route("/updateNetwork", methods=["POST"])
def updateNetwork():
    resp = jsonify(success=True)
    if request.method == "POST":
        new_map= request.json
        email = new_map['email_field']
        hosturl = new_map['host_url_field']
        email_db = Network.query.filter_by(email=email).first()
        if email_db is None:
            abort(404, f'email {email} does not exist')
        else:
            num_rows_updated = Network.query.filter_by(email=email).update(dict(hosturl=hosturl))
            db.session.commit()
            resp.status_code = 200
            return resp
    resp.status_code=404
    return resp

        
@app.route("/fetchHosts" , methods = ["GET"])
def fetchHosts():
    jsonres=[]
    results = Network.query.all()
    print("PRAJITH")
    
    for network in results:
        jsonres.append({"email":network.email,"hosturl":network.hosturl})
        print(network.email)
        print(network.hosturl)
    print(jsonres)
    return jsonify(jsonres)


@app.route("/")
def index():
    return "Hello World!"
