# Importing everything from enigma
from enigma.components import EnigmaCircuit, Rotor, Reflector, Plugboard
from cli import Cr_rotor, Cr_plugboard, Cr_reflector

# Importing from flask 
from flask import Flask, render_template, request, session, redirect, url_for

# Initiating flask app
app = Flask(__name__)
app.secret_key = "Ayman is a little dickhead to take all the credits on the slides"  # Needed for session handling


def SESSION_CHECKER():
        return (("rotors" in session["enigma_config"]) and 
        ("mode" in session["enigma_config"]) and 
        ("reflector" in session["enigma_config"]))


# Defining the form parsing function
def validate_and_parse_form(form):
        rotors = form.get("rotors", "").split()
        mode = form.get("mode", "").split()
        reflector_choice = form.get("reflector","").split()
        plugs = form.get("plugs", "").split()

        if not rotors or not mode or not reflector_choice:
                raise ValueError("rotor, mode and reflector ")
        if len(rotors) != len(mode):
                raise ValueError("Number of rotors and number of initial positions must match")
        for swap in plugs:
                if len(swap) != 2:
                        raise ValueError(f"Invalid plug swap : {swap}")
        return rotors, mode, reflector_choice, plugs

def build_circuit_from_session():
        cfg = session.get("enigma_config")
        if not cfg:
                raise RuntimeError("No enigma configuration found in session. Call /setup first.")
        rotor_objs = [Cr_rotor(model, window, idx) for idx, (model, window) in enumerate(zip(cfg["rotors"], cfg["mode"]))]
        reflector = Cr_reflector(cfg["reflector"])
        plugboard = Cr_plugboard(*cfg["plugs"])
        return EnigmaCircuit(rotor_objs, reflector, plugboard)


@app.route("/encrypt", methods = ["POST"])
def encrypt():
        try: 
                message = request.form.get("Message", "")
                if not message:
                        return(jsonify({"ok": False, "error": ""}))

                enigma = build_circuit_from_session()
                # Encrypt letter-by-letter, updating rotor windows as you go 
                ciphertext = "".join(enigma.Encryption(ch) for ch in message if ch.isalpha())

                # After encryption, capture updated rotor windows and save back to session
                updated_windows = [r.Window for r in enigma.Rotors]
                cfg = session["enigma_config"]
                cfg["mode"] = updated_windows
                session["enigma_config"] = cfg

                return jsonify({"ok": True, "ciphertext": ciphertext,"windows": updated_windows})
        except RuntimeError as e:
                return jsonify({"ok": False, "error" : "No message provided."}), 400

        except Exception as e:
                return jsonify({"ok": False, "error": "Internal error: " + str(e)}), 500



@app.route("/setup", methods = ["POST", "GET"])
def setup():
        if request.method == "GET":
                if not (SESSION_CHECKER()):
                        return render_template("setup.html")
                elif SESSION_CHECKER():
                        return redirect("{{url_for('machine')}}")

        elif request.method() == "POST":
                try:
                        rotors, mode, reflector_choice, plugs = validate_and_parse_form(request.form)
                except ValueError as e:
                        return jsonify({"ok": False, "error": str(e)}, 400)

                # Save configuration in session (safe serializable data)
                session["enigma_config"] = {
                        "rotors": rotors,
                        "mode": mode,
                        "reflector": reflector_choice,
                        "plugs": plugs
                }
                return jsonify({"ok": True, "message": "Configuration saved."})


@app.route("/machine", methods = ["POST", "GET"])
def machine():
        if request.method == "GET" and not (SESSION_CHECKER()):
                return redirect("{{url_for('index')}}")
        elif request.method == "GET" and (SESSION_CHECKER()):
                ...

        elif request.method == "POST":
                ...






if __name__ == "__main__":
        app.run(debug=True)