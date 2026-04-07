# Importing everything from enigma
from enigma.components import EnigmaCircuit, Rotor, Reflector, Plugboard

# Importing from flask 
from flask import Flask, render_template, request, session, redirect, url_for

# Initiating flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session handling

@app.route("/", methods=["GET", "POST"])
def setup():
    if request.method == "GET":
        return render_template("setup.html")
    if request.method == "POST":
        # Collect form data
        rotors = request.form.get("rotors").split()
        positions = request.form.get("positions").split()
        reflector = request.form.get("reflector")
        plugboard = request.form.get("plugboard").split()

        # Save configuration in session
        session["rotors"] = rotors
        session["positions"] = positions
        session["reflector"] = reflector
        session["plugboard"] = plugboard

        return redirect(url_for("machine"))

    # If already configured, go straight to machine
    if "rotors" in session:
        return redirect(url_for("machine"))

    return render_template("setup.html")


@app.route("/machine")
def machine():
    if "rotors" not in session:
        return redirect(url_for("setup"))

    # Build Enigma machine from session data
    rotors = [Rotor(model, window) for model, window in zip(session["rotors"], session["positions"])]
    reflector = Reflector(session["reflector"])
    plugboard = Plugboard(*session["plugboard"])
    machine = EnigmaCircuit(rotors, reflector, plugboard)

    # For now, just show empty output
    output = ""

    return render_template(
        "machine.html",
        rotors=" ".join(session["rotors"]),
        positions=" ".join(session["positions"]),
        reflector=session["reflector"],
        plugboard=" ".join(session["plugboard"]),
        output=output
    )


@app.route("/reset")
def reset():
    # Clear the session and go back to setup
    session.clear()
    return redirect(url_for("setup"))


if __name__ == "__main__":
    app.run(debug=True)
