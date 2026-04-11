# Importing stuff
import argparse
from pynput import keyboard

# Importing from my own module
from enigma.components import EnigmaCircuit, Rotor, Reflector, Plugboard

# Defining the Main function
def main():
    rotorConf, reflector, plugboard = setup_enigma()
    Machine = EnigmaCircuit(rotorConf, reflector, plugboard)
    print("Enigma Machine is ready. Press ESC to exit.")
    # For macWorks
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




# Access point
if __name__ == "__main__":
    main()
