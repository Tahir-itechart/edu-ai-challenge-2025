const { Enigma, Rotor, ROTORS, REFLECTOR } = require('./enigma.js');

describe('Enigma Machine Unit Tests', () => {
  
  describe('Constants', () => {
    test('ROTORS should be properly defined', () => {
      expect(ROTORS).toHaveLength(3);
      expect(ROTORS[0]).toHaveProperty('wiring');
      expect(ROTORS[0]).toHaveProperty('notch');
      expect(ROTORS[0].wiring).toHaveLength(26);
    });

    test('REFLECTOR should be properly defined', () => {
      expect(REFLECTOR).toHaveLength(26);
      expect(typeof REFLECTOR).toBe('string');
    });
  });

  describe('Rotor Class', () => {
    let rotor;

    beforeEach(() => {
      rotor = new Rotor(ROTORS[0].wiring, ROTORS[0].notch, 0, 0);
    });

    test('should initialize correctly', () => {
      expect(rotor.wiring).toBe(ROTORS[0].wiring);
      expect(rotor.notch).toBe(ROTORS[0].notch);
      expect(rotor.ringSetting).toBe(0);
      expect(rotor.position).toBe(0);
    });

    test('step should increment position correctly', () => {
      expect(rotor.position).toBe(0);
      rotor.step();
      expect(rotor.position).toBe(1);
    });

    test('step should wrap around at 26', () => {
      rotor.position = 25;
      rotor.step();
      expect(rotor.position).toBe(0);
    });

    test('atNotch should detect notch position correctly', () => {
      rotor.position = 16; // Q
      expect(rotor.atNotch()).toBe(true);
      rotor.position = 15;
      expect(rotor.atNotch()).toBe(false);
    });

    test('forward should transform characters correctly', () => {
      const result = rotor.forward('A');
      expect(typeof result).toBe('string');
      expect(result.length).toBe(1);
      expect(result.match(/[A-Z]/)).toBeTruthy();
    });

    test('backward should transform characters correctly', () => {
      const result = rotor.backward('E');
      expect(typeof result).toBe('string');
      expect(result.length).toBe(1);
      expect(result.match(/[A-Z]/)).toBeTruthy();
    });
  });

  describe('Enigma Class', () => {
    let enigma;

    beforeEach(() => {
      enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
    });

    test('should initialize correctly', () => {
      expect(enigma.rotors).toHaveLength(3);
      expect(enigma.plugboardPairs).toEqual([]);
    });

    test('stepRotors should step rightmost rotor', () => {
      const initialPos = enigma.rotors[2].position;
      enigma.stepRotors();
      expect(enigma.rotors[2].position).toBe(initialPos + 1);
    });

    test('encryptChar should handle non-alphabetic characters', () => {
      expect(enigma.encryptChar('1')).toBe('1');
      expect(enigma.encryptChar(' ')).toBe(' ');
      expect(enigma.encryptChar('!')).toBe('!');
    });

    test('encryptChar should encrypt alphabetic characters', () => {
      const result = enigma.encryptChar('A');
      expect(typeof result).toBe('string');
      expect(result.length).toBe(1);
      expect(result.match(/[A-Z]/)).toBeTruthy();
      expect(result).not.toBe('A');
    });

    test('process should handle empty string', () => {
      expect(enigma.process('')).toBe('');
    });

    test('process should convert to uppercase', () => {
      const result = enigma.process('hello');
      expect(result).toMatch(/^[A-Z\s\d\W]*$/);
    });
  });

  describe('Integration Tests', () => {
    test('should be symmetric without plugboard', () => {
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const plaintext = 'HELLO';
      const encrypted = enigma1.process(plaintext);
      const decrypted = enigma2.process(encrypted);
      expect(decrypted).toBe(plaintext);
    });

    test('should be symmetric with plugboard', () => {
      const plugPairs = [['A', 'B'], ['C', 'D']];
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], plugPairs);
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], plugPairs);
      const plaintext = 'HELLO';
      const encrypted = enigma1.process(plaintext);
      const decrypted = enigma2.process(encrypted);
      expect(decrypted).toBe(plaintext);
    });

    test('should be symmetric with different configurations', () => {
      const enigma1 = new Enigma([0, 1, 2], [5, 10, 15], [2, 4, 6], [['Q', 'W']]);
      const enigma2 = new Enigma([0, 1, 2], [5, 10, 15], [2, 4, 6], [['Q', 'W']]);
      const plaintext = 'TESTMESSAGE';
      const encrypted = enigma1.process(plaintext);
      const decrypted = enigma2.process(encrypted);
      expect(decrypted).toBe(plaintext);
    });

    test('should handle long messages', () => {
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const plaintext = 'THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG';
      const encrypted = enigma1.process(plaintext);
      const decrypted = enigma2.process(encrypted);
      expect(decrypted).toBe(plaintext);
    });

    test('should handle mixed characters', () => {
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const input = 'HELLO, WORLD! 123';
      const encrypted = enigma1.process(input);
      const decrypted = enigma2.process(encrypted);
      expect(decrypted).toBe(input);
      expect(encrypted).toContain(',');
      expect(encrypted).toContain('!');
      expect(encrypted).toContain(' ');
      expect(encrypted).toContain('123');
    });
  });

  describe('Edge Cases', () => {
    test('should not encrypt character to itself', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const encrypted = enigma.encryptChar('A');
      expect(encrypted).not.toBe('A');
    });

    test('should handle rotor stepping', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const initialPos = enigma.rotors[2].position;
      enigma.encryptChar('A');
      expect(enigma.rotors[2].position).toBe(initialPos + 1);
    });

    test('should handle different ring settings', () => {
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [5, 10, 15], []);
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const result1 = enigma1.encryptChar('A');
      const result2 = enigma2.encryptChar('A');
      // Results should be different due to ring settings
      expect(result1).not.toBe(result2);
    });
  });
}); 