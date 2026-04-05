# Importing stuff
import argparse
#import keyboard
from pynput import keyboard

# Defining the Main function
def main():
    rotorConf, reflector, plugboard = setup_enigma()
    Machine = EnigmaCircuit(rotorConf, reflector, plugboard)
    print("Enigma Machine is ready. Press ESC to exit.")
    
    def on_press(key):
        try:
            # handle normal character keys
            char = key.char.upper()
            if char.isalpha():
                print(Machine.Encryption(char))
        except AttributeError:
            #Handle special keys (like ESC)
            if key == keyboard.Key.esc:
                print("\nExiting...")
                return False #Stops the listener
            
    with keyboard.Listener(on_press=on_press, suppress=True) as listener:
        listener.join()
            





    #This block of code is in the previous version that does not work on macOS, only on windows because of lesser support of keyboard module
    """
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            char = str(event.name).strip().upper()
            if char == "ESC":
                print("\nExiting....")
                break
            elif len(char) == 1 and char.isalpha():
                print(Machine.Encryption(char))
    """






def setup_enigma():
    """
    Parses command-line arguments and sets up the Enigma machine components (rotors, reflector, and plugboard).
    """
    parser = argparse.ArgumentParser(description="Setting up the Enigma Machine.")

    # Command-line arguments for configuring the Enigma machine
    parser.add_argument("Plugs", metavar="Plug", nargs="*", help="Plugboard swaps (pairs of characters)")
    parser.add_argument("-R", "--rotors", nargs="+", help="Rotor models in order from left to right")
    parser.add_argument("-M", "--mode", nargs="+", help="Initial rotor window positions")
    parser.add_argument("--reflector", type=str, choices=["B", "C", "BT", "CT"], help="Reflector model")

    # Parse arguments
    args = parser.parse_args()

    # Creating Enigma components
    if args.rotors is None or args.mode is None:
        raise ValueError("Both --rotors and --mode arguments must be provided.")
    if len(args.rotors) != len(args.mode):
        raise ValueError("Number of rotors and number of initial positions must match.")
    # Validate plugboard swaps
    for swap in args.Plugs:
        if len(swap) != 2:
            raise ValueError(f"Each plugboard swap must be exactly two characters: '{swap}' is invalid.")
    plugboard = Cr_plugboard(*args.Plugs)
    reflector = Cr_reflector(args.reflector)
    rotors = [Cr_rotor(model, window, idx) for idx, (model, window) in enumerate(zip(args.rotors, args.mode))]

    return rotors, reflector, plugboard


# Defining the Wrapper funtions for creating all the Components.
def Cr_rotor(model, window, position = 0):
    return Rotor(model, window, position)   # Has check_passing and step method

def Cr_reflector(model):
    return Reflector(model)

def Cr_plugboard(*swaps):
    return Plugboard(*swaps)


# Defining the EnigmaCircuit Class.
class EnigmaCircuit:
    def __init__(self, rotors, reflector, plugboard):
        self.Rotors = rotors  # Loading the rotors (left to right)
        self.Reflector = reflector
        self.Plugboard = plugboard

    def step_rotors(self):
        # Implement notch-based stepping that produces the correct double-step behaviour.
        # Rotors are stored left->right in self.Rotors.
        # We only step before encoding a key press.
        n = len(self.Rotors)
        if n == 0:
            return

        # Determine which rotors should step.
        # Rightmost rotor always steps.
        to_step = [False] * n
        to_step[-1] = True

        # If rotor i (from left 0..n-1) is at notch, it causes rotor to its left to step on next keypress.
        # We check from right towards left to mark stepping caused by notches.
        # Proper behavior: if rotor i-1 is at notch, rotor i steps. That produces double-step for the middle rotor.
        for i in range(n - 1, 0, -1):
            if self.Rotors[i - 1].at_notch():
                to_step[i] = True

        # Apply steps
        for i in range(n):
            if to_step[i]:
                self.Rotors[i].step()

    def Encryption(self, character):
        character = self.Plugboard.passing(character)
        self.step_rotors()

        # Forward through rotors (rightmost first)
        for rotor in reversed(self.Rotors):
            character = rotor.entry_conversion(character)

        # Reflect
        character = self.Reflector.reflect(character)

        # Backward through rotors (left to right)
        for rotor in self.Rotors:
            character = rotor.exit_conversion(character)

        character = self.Plugboard.passing(character)
        return character


# Defining the Rotor class
class Rotor:
    # All the Rotors
    MODELS = {
    'ENTRY' : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # Rotor Right Side
    "I" : "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    'II' : "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    'III' : "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    'IV' : "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    'V' : "VZBRGITYUPSDNHLXAWMJQOFECK",
    'VI' : "JPGVOUMFYQBENHZRDKASXLICTW",
    'VII' : "NZJHGRCXMYSWBOUFAIVLPEKQDT",
    'VIII' : "FKQHTLXOCBJSPDZRAMEWNIUYGV",
    'BETA' : "LEYJVCNIXWPBQMDRTAKZGFUHOS",
    'GAMMA' : "FSOKANUERHMBTIYCWLQPZXVGJD",
    }

    # The notches (window letters) where the next rotor will move up
    WINDOWS = {
        "I" : list("Q"),
        "II" : list("E"),
        "III" : list("V"),
        "IV" : list("J"),
        "V" : list("H"),
        "VI" : ["H", "U"],
        "VII" : ["H", "U"],
        "VIII" : ["H", "U"],
    }

    # Defining the __init__ method
    def __init__(self, model, window, position = 0):
        self.Access = Rotor.MODELS["ENTRY"]  # Right side alphabet
        self.Position = position  # Not used currently for ring settings but kept
        self.Model = model.upper().strip()
        if self.Model not in Rotor.MODELS:
            raise ValueError(f"This program only supports the following rotor models: {', '.join(Rotor.MODELS)}.")
        self.Rotor = Rotor.MODELS[self.Model]  # Wiring mapping right->left as string
        # Build inverse mapping for reverse path (left->right)
        self.InverseMap = { self.Rotor[i]: self.Access[i] for i in range(26) }
        self.Window = window.upper().strip()  # The visible letter in the window
        self.Pass = False  # not used for stepping now (kept for compatibility)

    def at_notch(self):
        # Return True if rotor is currently on a notch position that causes left rotor to step
        notches = Rotor.WINDOWS.get(self.Model, [])
        return self.Window in notches

    def entry_conversion(self, character):
        # Forward pass through rotor (right->left)
        # Convert input letter to index on Access, apply rotation offset, map through rotor wiring,
        # then return the letter in the rotor's left side reference (which will then be fed to next stage).
        offset = self.Access.index(self.Window)
        in_idx = self.Access.index(character)
        stepped = (in_idx + offset) % 26
        mapped = self.Rotor[stepped]               # letter on left side
        # To feed into next component (reflector or next rotor), convert mapped letter back into Access alphabet
        # by finding its index in rotor left side wiring and then adjusting back by offset.
        # BUT since we return a letter, simply return mapped; caller interprets letters consistently.
        return mapped

    def exit_conversion(self, character):
        # Backward pass through rotor (left->right)
        # Use inverse mapping to find corresponding right-side contact, then account for rotor offset.
        offset = self.Access.index(self.Window)
        # character is letter seen on rotor left side; find corresponding right-side letter
        if character not in self.InverseMap:
            # Should not happen if wiring is consistent
            raise ValueError(f"Character {character} not found in inverse mapping of rotor {self.Model}")
        mapped_right = self.InverseMap[character]  # letter on right side before offset correction
        # Now we must convert mapped_right to the "external" alphabet accounting for offset
        # Find index in Access (mapped_right index), then remove offset to get outgoing letter
        out_idx = (self.Access.index(mapped_right) - offset) % 26
        return self.Access[out_idx]

    def check_passing(self):
        return self.Pass

    def step(self):
        # Rotate the window one step forward
        self.Window = self.Access[(self.Access.index(self.Window) + 1) % 26]


# Defining the Reflector class
class Reflector:
    REFLECTORS = ["B", "C", "BT", "CT", ]  # Supported Reflector Models.
    CONTACTS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    C = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    BT = "ENKQAUYWJICOPBLMDXZVFTHRGS"
    CT = "RDOBJNTKVEHMLFCWZAXGYIPSUQ"

    def __init__(self, reflector):
        self.entry = Reflector.CONTACTS
        if not reflector in Reflector.REFLECTORS:
            raise ValueError(f"This program only supports the following Reflector Models: {', '.join(Reflector.REFLECTORS)}.")
        self.conf = getattr(self, reflector.upper().strip())

    def reflect(self, character):
        return self.conf[self.entry.index(character)]


# Defining the Plugboard class
class Plugboard:
    def __init__(self, *swaps):
        self.swaps = set(swaps)

    def passing(self, character):
        character = character.upper().strip()
        if not self.swaps:
            return character
        for x in self.swaps:
            if character in x:
                return x[x.index(character) - 1]
        return character

    @property
    def swaps(self):
        return self._swaps

    @swaps.setter
    def swaps(self, swaps):
        if len(swaps) > 10:
            raise ValueError("Plugboard can only have up to 10 swaps.")
        if any(len(pair) != 2 for pair in swaps):
            raise ValueError("Each swap must be exactly two characters.")
        if len(set("".join(swaps))) != len("".join(swaps)):  # Prevent duplicate characters
            raise ValueError("A character cannot be swapped more than once.")
        self._swaps = set(swaps)


# Access point
if __name__ == "__main__":
    main()
