import { CPUPlayer } from '../player.js';

describe('CPUPlayer', () => {
    let cpu;

    beforeEach(() => {
        cpu = new CPUPlayer();
    });

    test('should start in "hunt" mode', () => {
        expect(cpu.mode).toBe('hunt');
    });

    test('generateGuess should return a valid coordinate string', () => {
        const guess = cpu.generateGuess();
        expect(guess).toMatch(/^[0-9]{2}$/);
    });

    test('generateGuess should not repeat guesses in hunt mode', () => {
        const guesses = new Set();
        // Generate a large number of guesses to check for duplicates
        for (let i = 0; i < 50; i++) {
            const guess = cpu.generateGuess();
            expect(guesses.has(guess)).toBe(false);
            guesses.add(guess);
        }
    });

    test('updateAfterHit should switch to "target" mode when a ship is hit but not sunk', () => {
        cpu.updateAfterHit('33', false); // wasSunk = false
        expect(cpu.mode).toBe('target');
    });

    test('updateAfterHit should add adjacent squares to the target queue', () => {
        cpu.updateAfterHit('33', false);
        // Should contain '23', '43', '32', '34' in some order
        expect(cpu.targetQueue).toHaveLength(4);
        expect(cpu.targetQueue).toContain('23');
        expect(cpu.targetQueue).toContain('43');
        expect(cpu.targetQueue).toContain('32');
        expect(cpu.targetQueue).toContain('34');
    });

    test('updateAfterHit should switch back to "hunt" mode when a ship is sunk', () => {
        // Get into target mode first
        cpu.updateAfterHit('33', false);
        expect(cpu.mode).toBe('target');

        // Now sink the ship
        cpu.updateAfterHit('34', true); // wasSunk = true
        expect(cpu.mode).toBe('hunt');
        expect(cpu.targetQueue).toHaveLength(0);
    });

    test('generateGuess should use the target queue when in target mode', () => {
        cpu.updateAfterHit('55', false);
        const nextGuess = cpu.generateGuess();
        // The guess should be one of the adjacent cells
        expect(['45', '65', '54', '56']).toContain(nextGuess);
        expect(cpu.targetQueue).toHaveLength(3);
    });

    test('generateGuess should revert to hunt mode if target queue becomes empty', () => {
        cpu.updateAfterHit('55', false); // mode -> target
        cpu.generateGuess(); // guess '45', queue length 3
        cpu.generateGuess(); // guess '65', queue length 2
        cpu.generateGuess(); // guess '54', queue length 1
        cpu.generateGuess(); // guess '56', queue length 0
        
        expect(cpu.mode).toBe('hunt'); // mode should switch back
        
        const huntGuess = cpu.generateGuess();
        // This should be a random guess, not from the now-empty queue
        expect(cpu.guesses.has(huntGuess)).toBe(true);
    });
}); 