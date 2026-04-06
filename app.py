#Importing everything form enigma
import enigma

#Importing from flask 
from flask import Flask, render_template, request


#Initiating flask app
app = Flask(__name__)


#Setup route
@app.route("/", methods=["POST", "GET"])
def setup():
    if request.method() == "GET":
        ...

    if request.method() == "POST":
        ...