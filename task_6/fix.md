# Enigma Machine Bug Fix

## Bug Description

The Enigma machine implementation had a critical bug in the plugboard functionality that prevented correct encryption/decryption symmetry. 

**Symptoms:**
- Messages encrypted and decrypted with **no plugboard settings** worked correctly
- Messages encrypted and decrypted with **plugboard settings** failed to decrypt back to the original plaintext
- Example: "HELLO" with plugboard `[['A', 'B']]` would encrypt to "VNACA" but decrypt to "HEYLK" instead of "HELLO"

## Root Cause

The bug was in the `encryptChar` method of the `Enigma` class. The plugboard transformation was only applied **once** (before entering the rotors), but in a real Enigma machine, the electrical signal passes through the plugboard **twice**:

1. **First pass**: Before entering the rotors (input transformation)
2. **Second pass**: After exiting the rotors and reflector (output transformation)

### Buggy Code (Before Fix)
```javascript
encryptChar(c) {
    if (!alphabet.includes(c)) return c;
    this.stepRotors();
    c = plugboardSwap(c, this.plugboardPairs);  // ❌ Only applied once!
    
    // Forward through rotors
    for (let i = this.rotors.length - 1; i >= 0; i--) {
        c = this.rotors[i].forward(c);
    }

    // Reflector
    c = REFLECTOR[alphabet.indexOf(c)];

    // Backward through rotors
    for (let i = 0; i < this.rotors.length; i++) {
        c = this.rotors[i].backward(c);
    }

    return c;  // ❌ Missing second plugboard application
}
```
