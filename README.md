# ODYSSEY ENIGMA (Enigma Machine Simulator)

## Video Demo: <https://youtu.be/9F7QoQ1kr0s>

A Python-based implementation of the famous Enigma cipher machine, allowing users to encrypt messages using the same encryption mechanism employed during World War II.

## Overview

This project simulates the Enigma machine, an electromechanical rotor cipher device that was historically used for encrypting military communications. The implementation includes all the core components: rotors, a reflector, and a plugboard, providing a fully functional encryption system.

## Features

- **Multiple Rotor Models**: Supports rotors I-VIII, BETA, and GAMMA with authentic Enigma wiring configurations
- **Configurable Reflectors**: Includes four reflector models (B, C, BT, CT) for different encryption profiles
- **Plugboard Support**: Implement up to 10 character-pair swaps to add an additional encryption layer
- **Authentic Rotor Stepping**: Implements proper notch-based rotor stepping with correct double-step behavior
- **Real-time Encryption**: Interactive keyboard-based interface for live message encryption

## Usage

Run the Enigma machine simulator with the following command:

```bash
sudo python3 enigma.py -R [rotor models] -M [starting positions] --reflector [reflector model] [plugboard swaps]
```

### Arguments

- `-R, --rotors`: Space-separated rotor models in order from left to right (required)
  - Available: `I`, `II`, `III`, `IV`, `V`, `VI`, `VII`, `VIII`, `BETA`, `GAMMA`
  
- `-M, --mode`: Initial rotor window positions for each rotor (required)
  - Must be one letter (A-Z) per rotor, matching the number of rotors specified
  
- `--reflector`: Reflector model (required)
  - Available: `B`, `C`, `BT`, `CT`
  
- `Plugs`: Optional positional arguments for plugboard swaps
  - Specify as pairs of characters (e.g., `AB CD EF` swaps A↔B, C↔D, E↔F)
  - Maximum 10 swaps allowed

### Examples

**Basic setup with three rotors:**

```bash
sudo python enigma.py -R I II III -M A A A --reflector B
```

**With plugboard configuration:**

```bash
sudo python enigma.py -R I II III -M Q E V --reflector B AB CD EF
```

**With rotors VI, VII, VIII:**

```bash
sudo python enigma.py -R VI VII VIII -M A A A --reflector C GH IJ KL MN OP QR
```

## How It Works

### Encryption Process

When you press a key on the keyboard:

1. **Plugboard**: The character passes through the plugboard, where specified pairs are swapped
2. **Rotor Stepping**: Rotors advance according to notch positions before encryption (rightmost always steps)
3. **Forward Path**: Signal passes through rotors from right to left, with each rotor applying its wiring transformation
4. **Reflection**: The signal bounces off the reflector, creating reciprocal encryption
5. **Backward Path**: Signal passes through rotors again from left to right using inverse wiring
6. **Plugboard Output**: Final character passes through plugboard again and displays

The beauty of Enigma is that **the same settings used to encrypt will decrypt** — the reciprocal path through the reflector ensures symmetric encryption.

### Rotor Mechanics

- Each rotor has 26 contacts and an internal wiring that maps one letter to another
- Rotors rotate after each keypress, changing the encryption mapping
- When a rotor reaches a "notch" position, it causes the rotor to its left to step on the next keypress
- This creates the famous **double-stepping** behavior where the middle rotor can step two positions in succession

## Components

### Rotor

Implements the core encryption logic with:

- Configurable wiring (10 different historical models)
- Notch positions that trigger adjacent rotor stepping
- Entry/exit conversion methods for forward and backward signal paths

### Reflector

Bounces the signal back through the rotors using one of four historical reflector wirings, ensuring message encryption is symmetric.

### Plugboard

Provides an initial substitution layer with up to 10 character-pair swaps, adding complexity to the encryption before rotor processing.

### EnigmaCircuit

Orchestrates the complete encryption pipeline, managing rotor stepping and signal flow through all components.

## Limitations

- Maximum 10 plugboard swaps
- Rotors must have matching number of models and starting positions
- Requires administrator privileges due to keyboard library dependencies

## Historical Context

The Enigma machine was famously broken by codebreakers at Bletchley Park during WWII, notably including Alan Turing. This implementation provides a functional simulator to understand the mechanical principles behind one of history's most important cryptographic devices.

## Requirements

- Python 3.6+
- `pynput` library

## License

This project is provided as an educational tool for understanding cipher machines and cryptography.

## Author

Created by [navid-nowroz](https://github.com/navid-nowroz)
