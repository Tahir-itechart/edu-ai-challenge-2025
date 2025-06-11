import { Ship } from '../ship.js';

describe('Ship', () => {
    let ship;

    beforeEach(() => {
        ship = new Ship(['01', '02', '03']);
    });

    test('should initialize with correct locations and no hits', () => {
        expect(ship.locations).toEqual(['01', '02', '03']);
        expect(ship.hits).toEqual([false, false, false]);
    });

    test('isSunk() should return false for a new ship', () => {
        expect(ship.isSunk()).toBe(false);
    });

    test('recordHit() should mark a location as hit', () => {
        const result = ship.recordHit('02');
        expect(result).toBe(true);
        expect(ship.hits).toEqual([false, true, false]);
    });

    test('recordHit() should return false for a missed location', () => {
        const result = ship.recordHit('11');
        expect(result).toBe(false);
        expect(ship.hits).toEqual([false, false, false]);
    });

    test('isSunk() should return true when all locations are hit', () => {
        ship.recordHit('01');
        ship.recordHit('02');
        ship.recordHit('03');
        expect(ship.isSunk()).toBe(true);
    });
}); 