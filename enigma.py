# Importing stuff
import argparse
import keyboard


# Defining the Main function
def main():
    rotorConf, reflector, plugboard = setup_enigma()
    Machine = EnigmaCircuit(rotorConf, reflector, plugboard)

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            char = str(event.name).strip().upper()
            if char == "ESC":
                print("\nExiting....")
                break
            elif len(char) == 1 and char.isalpha():
                print(Machine.Encryption(char))

def setup_enigma():
    parser = argparse.ArgumentParser(description="Setting up the Enigma Machine.")

    # Command-line arguments for configuring the Enigma machine
    parser.add_argument("Plugs", metavar="Plug", nargs="*", help="Plugboard swaps (pairs of characters)")
    parser.add_argument("-R", "--rotors", nargs="+", help="Rotor models in order from left to right")
    parser.add_argument("-M", "--mode", nargs="+", help="Initial rotor window positions")
    parser.add_argument("--reflector", type=str, choices=["B", "C", "BT", "CT"], help="Reflector model")

    # Parse arguments
    args = parser.parse_args()

    # Creating Enigma components
    rotors = [Cr_rotor(model, window) for model, window in zip(args.rotors, args.mode)]
    reflector = Cr_reflector(args.reflector)
    plugboard = Cr_plugboard(*args.Plugs)

    return rotors, reflector, plugboard




# Defining the Wrapper funtions for creating all the Components.
def Cr_rotor(model, window, position = 0):
    return Rotor(model, window, position)   # Has check_passing and step method

def Cr_reflector(model):
    return Reflector(model)

def Cr_plugboard(*swaps):
    return Plugboard(swaps)




# Defining the EnigmaCircuit Class.
class EnigmaCircuit:
    def __init__(self, rotors, reflector, plugboard):
        self.Rotors = rotors  # Loading the rotors
        self.Reflector = reflector
        self.Plugboard = plugboard


    def step_rotors(self):
        for i in range(len(self.Rotors) - 1, 0, -1):
            if self.Rotors[i - 1].check_passing():
                self.Rotors[i].step()
        self.Rotors[-1].step()

    def Encryption(self, character):
        character = self.Plugboard.passing(character)
        self.step_rotors()
        for rotor in reversed(self.Rotors):
            character = rotor.entry_conversion(character, rotor.Window)
        character = self.Reflector.reflect(character)
        for rotor in self.Rotors:
            character = rotor.exit_conversion(character, rotor.Window)
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

    # The widows where the next rotor will move up
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
        self.Access = Rotor.MODELS["ENTRY"]  # Right side of the Rotor
        self.Position = position  # The position for the rotor
        self.Model = model.upper().strip()
        if self.Model not in Rotor.MODELS:
            raise ValueError(f"This program only supports the following rotor models: {', '.join(Rotor.MODELS)}.")
        self.Rotor = Rotor.MODELS[self.Model]  # Left side of the Rotor.
        self.Window = window.upper().strip()  # The window for the operatior to see in the enigma machine.
        self.Pass = False


    def entry_conversion(self, character, step):
        step = self.Access.index(self.Window)  # Getting the steps
        int_entry = self.Access.index(character)  # Getting the character
        int_exit = (int_entry + step) % 26  # Processing through integer conversion
        end_char = self.Rotor[int_exit]
        return end_char  # Returning the End Character

    def exit_conversion(self, character, step):
        step = self.Access.index(self.Window)  # Getting the steps
        int_entry = self.Access.index(character)  # Getting the character
        int_exit = (int_entry - step) % 26  # Processing through integer conversion
        end_char = self.Rotor[int_exit]
        if self.Position == 0:
            self.step()
        elif self.Window in Rotor.WINDOWS[self.Model]:
            self.Pass = True
        else:
            self.Pass = False
        return end_char  # Returning the End Character

    def check_passing(self):
        return self.Pass

    def step(self):
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
