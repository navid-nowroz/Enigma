# Importing everything from enigma
from enigma.components import EnigmaCircuit, Rotor, Reflector, Plugboard

# Importing from flask 
from flask import Flask, render_template, request, session, redirect, url_for

# Initiating flask app
app = Flask(__name__)
app.secret_key = "Ayman is a little dickhead to take all the credits on the slides"  # Needed for session handling


@app.route("/", method = ["POST", "GET"])
def index():
        if request.method() == "GET":
                if not (("rotor_models" in session) and ("windows" in session) and ("reflector" in session)):
                        return render_template("setup.html")

        elif request.method() == "POST":
                ...