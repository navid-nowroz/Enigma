# Importing everything from enigma
from enigma.components import EnigmaCircuit, Rotor, Reflector, Plugboard
from cli import Cr_rotor, Cr_plugboard, Cr_reflector

# Importing from flask 
from flask import Flask, render_template, request, session, redirect, url_for

# Initiating flask app
app = Flask(__name__)
app.secret_key = "Ayman is a little dickhead to take all the credits on the slides"  # Needed for session handling


# Defining the form parsing function
def validate_and_parse_form(form):
        rotors = form.get("rotors", "").split(",")
        mode = form.get("mode", "").split(",")
        reflector_choice = form.get("reflector","").split(",")
        plugs = form.get("plugs", "").split()

        if not rotors or not mode or not reflector_choice:
                raise ValueError("rotor, mode and reflector ")
        if len(rotors) != len(mode):
                raise ValueError("Number of rotors and number of initial positions must match")
        for swap in plugs:
                if len(swap) != 2:
                        raise ValueError(f"Invalid plug swap : {swap}")
        return rotors, mode, reflector_choice, plugs


@app.route("/", methods = ["POST", "GET"])
def index():
        if request.method() == "GET":
                if not (("rotor_models" in session) and ("windows" in session) and ("reflector" in session)):
                        return render_template("setup.html")
                elif ("rotor_models" in session) and ("windows" in session) and ("reflector" in session):
                        return redirect("{{url_for('machine')}}")

        elif request.method() == "POST":
                ...


@app.route("/machine", methods = ["POST", "GET"])
def machine():
        if request.method() == "GET" and not (("rotor_models" in session) and ("windows" in session) and ("reflector" in session)):
                return redirect("{{url_for('index')}}")
        elif request.method() == "GET" and (("rotor_models" in session) and ("windows" in session) and ("reflector" in session)):
                ...

        elif request.method() == "POST":
                ...






if __name__ == "__main__":
        app.run(debug=True)